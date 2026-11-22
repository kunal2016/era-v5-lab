"""Item 11, code packs: recall of v1's code-token qualifying pairs (overlap_matches.csv, code/code, Jaccard >= 0.85)."""
import os
OUT = os.environ.get("MH_OUT", "out/minhash_item11")
import glob, json, numpy as np, pandas as pd, pyarrow.parquet as pq
R = os.environ.get("OVERLAP_RUN", "out/overlap_tsai") + "/"
docs = pq.read_table(R + "overlap_docs.parquet", columns=["doc_id", "pack", "split", "row"]).to_pandas()
rows, S, lines = [], [], []
for f in sorted(glob.glob(OUT + "/csig_*_train_*.npz")):
    z = np.load(f); pack = os.path.basename(f).split("csig_", 1)[1].rsplit("_", 2)[0]
    sub = docs[(docs.pack == pack) & (docs.split == "train")][["doc_id", "row"]]
    mm = pd.DataFrame({"doc_id": z["ids"]}).merge(sub, on="doc_id", how="left", validate="one_to_one")
    assert mm.row.notna().all(), f
    rows.append(mm.row.to_numpy()); S.append(z["sig"]); lines.append(z["lines"])
rows = np.concatenate(rows); S = np.concatenate(S); lines = np.concatenate(lines)
elig = (lines >= 20) & ~(S == np.iinfo(np.uint64).max).all(axis=1)   # code_scores only scores these
pos = {r: i for i, r in enumerate(rows)}
m = pd.read_csv(R + "overlap_matches.csv")
m = m[m.row_a.isin(pos) & m.row_b.isin(pos) & m.pack_a.str.startswith("code-") & m.pack_b.str.startswith("code-")]
ia, ib = m.row_a.map(pos).to_numpy(), m.row_b.map(pos).to_numpy()
h2 = (m.rule == "H2").to_numpy()
est = (S[ia[h2]] == S[ib[h2]]).mean(axis=1)
out = {"packs": sorted({p for p in docs.pack if p in ("code-rust", "code-python", "code-go")}),
       "documents": int(len(rows)), "eligible_20_lines": int(elig.sum()),
       "qualifying": m.groupby(["rule", "pack_a"]).size().astype(int).to_dict().__repr__(),
       "minhash_error_H2": {"mean_abs": float(np.abs(est - m.code_jaccard[h2]).mean()),
                            "p95_abs": float(np.quantile(np.abs(est - m.code_jaccard[h2]), 0.95))}, "configs": []}
for b, r in [(32, 4), (25, 5), (21, 6), (16, 8)]:
    hit = np.zeros(len(m), bool); cand = 0
    for i in range(b):
        band = np.ascontiguousarray(S[:, i * r:(i + 1) * r])
        h = band.view(np.dtype((np.void, 8 * r))).ravel()
        hit |= h[ia] == h[ib]
        _, c = np.unique(h[elig], return_counts=True); cand += int((c * (c - 1) // 2).sum())
    out["configs"].append({"bands": b, "rows": r, "candidate_pairs_upper": cand,
                           "recall_H2": round(float(hit[h2].mean()), 4),
                           "recall_H1": round(float(hit[~h2].mean()), 4) if (~h2).any() else None,
                           "missed_H2": m[h2 & ~hit][["pack_a", "code_jaccard"]].round(3).values.tolist()})
json.dump(out, open(OUT + "/results_code.json", "w"), indent=1); print(json.dumps(out, indent=1))
