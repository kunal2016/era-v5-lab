Device `cpu`, float32, TF32 off, P = 32, 131,072 ids per run. Reference: decode_ref.decode, float64, CPU, float32 CPU codes; reference ids equal 0..V-1: True.

| batch size | runs | hashes match | sha256 (run 1) | ids equal to reference (every run) | seconds per run |
|---|---|---|---|---|---|
| 1 | 3 | yes | `f373cee371bea349…` | yes | 294.0, 319.5, 278.9 |
| 7 | 3 | yes | `44ebe69e4061b552…` | yes | 80.4, 81.2, 80.9 |
| 4096 | 3 | yes | `f24afbd717b6383d…` | yes | 86.2, 85.1, 85.3 |
