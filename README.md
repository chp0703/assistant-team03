# Study Assistant — starter

A starter repository for the CSC10014 Smart Virtual Assistant project.

## Team Information

- **Class:** 25C02
- **Team:** 03

## Prerequisites

- Python >= 3.10
- Git

## Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/chp0703/assistant-team03.git
   cd assistant-team03
   ```
2. **Create & activate virtual environment:**
   - Windows (PowerShell):

```bash
     python -m venv .venv
     .venv\Scripts\Activate.ps1
```

- macOS / Linux / Git Bash:

```bash
  python3 -m venv .venv
  source .venv/bin/activate
```

- Install dependencies:

```bash
  pip install -r requirements.txt
  pip install -e .
```

## Run

```bash
python -m assistant "where is the training office?"
```

## Test

```bash
pytest -q
```

## Project structure

- data/: Sample datasets and data sources.

- docs/: Project documentation, team info, and reports.

- scripts/: Environment verification and utility scripts.

- src/: Main source code for the virtual assistant application.

- tests/: Automated unit and smoke tests.

- ui/: User interface components and assets.

- requirements.txt: Pinned project dependencies.

- pyproject.toml: Build system and package configuration.
