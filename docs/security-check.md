# Repository Security Check

Checked on 2026-10-16.

## Scope and method

- Manually reviewed tracked source code, configuration, documentation, tests, and sample data for credentials and personal information.
- Scanned the repository's Git history with Gitleaks 8.30.1:

  ```sh
  gitleaks git --redact --report-path /tmp/gitleaks-report.json .
  ```

## Results

- **Secrets:** Gitleaks reported no leaks in the 15 commits scanned. The manual review also found no API keys, passwords, access tokens, or private keys in the current files.
- **Personal information:** The previous `docs/team.md` listed team members' names and student numbers. This change removes that roster from the current tree.
- **Git history:** The earlier roster remains in existing Git history. This change does not rewrite shared history; repository maintainers would need to coordinate any history cleanup separately.

## Limits

This check covers repository files and Git history. It does not inspect GitHub secrets/settings, local environment files, or external services.
