# Step 2 vs Step 3 metrics

Authoritative assignment gate: `0.70`.

The local Step 2 candidate is now compliant at `0.7000`; no remote Step 2 or Step 3 run was generated in the current local-only pass. The historical remote values below remain superseded intermediate evidence under the old `0.68` gate.

| Metric | Step 2 | Step 3 |
|---|---:|---:|
| training rows | 2998 | 5996 |
| validation accuracy | 0.6767 | 0.7233 (historical) |
| held-out accuracy | 0.7000 (local) | 0.7480 (historical) |
| weighted F1 | 0.6988602225 (local) | 0.7470636556 (historical) |
| Actions run | pending | 32453289515 (superseded) |
| 0.70 compliance | local pass; remote pending | not established remotely |

Step 3 was triggered by the pointer-only commit `1748341334a78e688dcc270d32d750e900724612`.
