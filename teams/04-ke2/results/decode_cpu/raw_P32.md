Device `cpu`, float32, TF32 off, P = 32, 131,072 ids per run. Reference: decode_ref.decode, float64, CPU, float32 CPU codes; reference ids equal 0..V-1: True.

| batch size | runs | hashes match | sha256 (run 1) | ids equal to reference (every run) | seconds per run |
|---|---|---|---|---|---|
| 1 | 3 | yes | `f373cee371bea349…` | yes | 274.9, 274.4, 274.4 |
| 7 | 3 | yes | `44ebe69e4061b552…` | yes | 81.4, 81.1, 81.5 |
| 4096 | 3 | yes | `f24afbd717b6383d…` | yes | 90.6, 89.0, 90.2 |

ID hash in `decode_gpu.py`'s format (`ke2-decode-gpu-ids-v1`), the same in every run: `31c8d0e0ac50cff5c8021f88a2b608de2298fdbf216c620a40e83d2adbe26f9a`. Compare with `results/decode_gpu/raw_P32_sha256.txt`.
