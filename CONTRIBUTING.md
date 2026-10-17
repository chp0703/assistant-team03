# Contributing

## Secrets

- Never commit API keys, passwords, access tokens, private keys, or other credentials.
- Keep local credentials in `.env`. This file is ignored by Git; do not remove it from `.gitignore`.
- Copy `.env.example` to `.env` and fill in values on your machine. Keep `.env.example` limited to variable names and non-secret placeholders.
- Do not paste credentials into source code, logs, issues, pull requests, screenshots, or chat messages.
- If a credential is exposed, revoke or rotate it immediately, remove it from the working tree, and notify the repository maintainers. Deleting the file in a later commit does not remove it from Git history.
- Before opening a pull request, check the diff for secrets and personal data.
