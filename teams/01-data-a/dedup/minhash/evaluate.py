"""Item 11: how many of v1's exact-Jaccard pairs does MinHash + LSH find, at what candidate cost.
Ground truth: TSAI's 5 Nov overlap run on the same cleaned files (overlap_pairs.csv >= 0.50, overlap_matches.csv)."""
import os
OUT = os.environ.get("MH_OUT", "out/minhash_item11")
import glob, json, numpy as np, pandas as pd, pyarrow.parquet as pq
R = os.environ.get("OVERLAP_RUN", "out/overlap_tsai") + "/"
docs = pq.read_table(R + "overlap_docs.parquet").to_pandas()
key = {}
sig_rows, sigs, packs = [], [], []
for f in sorted(glob.glob(OUT + "/sig_*_train_*.npz")):
    z = np.load(f)
    pack = os.path.basename(f).split("sig_", 1)[1].rsplit("_", 2)[0]
    sub = docs[(docs.pack == pack) & (docs.split == "train")][["doc_id", "row", "shingles"]]
    mm = pd.DataFrame({"doc_id": z["ids"], "n": z["n"]}).merge(sub, on="doc_id", how="left", validate="one_to_one")
    assert (mm.shingles == mm.n).all(), f
    rows = mm.row.to_numpy()
    sig_rows.append(rows); sigs.append(z["sig"]); packs += [pack] * len(rows)
rows = np.concatenate(sig_rows); S = np.concatenate(sigs); empty = (S == np.iinfo(np.uint64).max).all(axis=1)
pos = {r: i for i, r in enumerate(rows)}
packset = sorted(set(packs))
pairs = pd.read_csv(R + "overlap_pairs.csv")
pairs = pairs[pairs.row_a.isin(pos) & pairs.row_b.isin(pos)].copy()
m = pd.read_csv(R + "overlap_matches.csv")
m = m[m.row_a.isin(pos) & m.row_b.isin(pos)].copy()
ia, ib = pairs.row_a.map(pos).to_numpy(), pairs.row_b.map(pos).to_numpy()
est = (S[ia] == S[ib]).mean(axis=1)
pairs["minhash_j"] = est
out = {"packs": packset, "documents": int(len(rows)), "empty": int(empty.sum()),
       "pairs_ge_0.50": int(len(pairs)), "qualifying": {k: int(v) for k, v in m.rule.value_counts().items()},
       "minhash_error": {"mean_abs": float(np.abs(est - pairs.jaccard).mean()),
                         "p95_abs": float(np.quantile(np.abs(est - pairs.jaccard), 0.95))}, "configs": []}
mia, mib = m.row_a.map(pos).to_numpy(), m.row_b.map(pos).to_numpy()
P = S.shape[1]
for b, r in [(64, 2), (42, 3), (32, 4), (25, 5), (21, 6), (16, 8), (8, 16)]:
    hit_p = np.zeros(len(pairs), bool); hit_m = np.zeros(len(m), bool); cand = 0
    for i in range(b):
        band = S[:, i * r:(i + 1) * r]
        h = np.ascontiguousarray(band).view(np.dtype((np.void, band.dtype.itemsize * r))).ravel()
        hit_p |= h[ia] == h[ib]; hit_m |= h[mia] == h[mib]
        _, counts = np.unique(h[~empty], return_counts=True)
        cand += int((counts * (counts - 1) // 2).sum())
    thr = (1 / b) ** (1 / r)
    cfg = {"bands": b, "rows": r, "threshold_approx": round(thr, 3), "candidate_pairs_upper": cand}
    for t in (0.5, 0.7, 0.8, 0.9):
        sel = pairs.jaccard >= t
        cfg[f"recall_pairs_ge_{t}"] = round(float(hit_p[sel].mean()), 4) if sel.any() else None
    for rule in ("H1", "H2"):
        sel = (m.rule == rule).to_numpy()
        cfg[f"recall_{rule}"] = round(float(hit_m[sel].mean()), 4) if sel.any() else None
    sel = (m.rule == "H2").to_numpy() & (m.word_jaccard.fillna(0) >= 0.5).to_numpy()
    cfg["recall_H2_word"] = round(float(hit_m[sel].mean()), 4) if sel.any() else None
    cfg["H2_missed_by_pack"] = m[(m.rule == "H2") & ~hit_m].pack_a.value_counts().to_dict()
    out["configs"].append(cfg)
json.dump(out, open(OUT + "/results.json", "w"), indent=1)
print(json.dumps(out, indent=1))
