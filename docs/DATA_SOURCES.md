# Data Sources and Owners

| Data                          | Source                   | Owner        | Update responsibility |
| ----------------------------- | ------------------------ | ------------ | --------------------- |
| Office names, rooms and hours | `data/offices.csv`       | Data team    | phkhoiit-1508         |
| Assistant behavior            | `src/assistant/rules.py` | Backend team | dmh612                |
| Smoke tests                   | `tests/test_smoke.py`    | QA team      | phkhoiit-1508         |

## Data update process

1. Propose a change in a GitHub issue.
2. Update the data through a feature branch.
3. Add or update a test when behavior changes.
4. Open a pull request for review.
5. Merge only after approval.
