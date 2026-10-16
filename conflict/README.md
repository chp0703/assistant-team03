# Controlled conflict drill

Run in pairs. Both partners start from the same commit of `main`.

1. Both: `git switch main && git pull`
2. Partner A: `git switch -c conflict/a-greeting`, edit `src/assistant/rules.py`, change the greeting line to
   `return "Hello! I can find offices and opening hours."` — commit, push, open PR.
3. Partner B: `git switch -c conflict/b-greeting`, edit the same line to
   `return "Hi there! Ask me about any campus office."` — commit, push, open PR.
4. Merge Partner A's PR (after review).
5. Partner B: `git fetch origin && git merge origin/main` → CONFLICT in rules.py.
6. Together, decide the final sentence, remove the markers, update `tests/test_smoke.py` if needed,
   run `pytest -q`, commit the merge with a message explaining the decision, push, get approval, merge.
