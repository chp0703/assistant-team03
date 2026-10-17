# Study Assistant — starter

A starter repository for the CSC10014 Smart Virtual Assistant project.

## Team Information

- **Class:** 25C02
- **Team:** 03

## Prerequisites

- Python >= 3.10
- Git

## Setup

Prerequisites: Python 3.10+, Git.

    git clone git@github.com:<you>/lab01-starter.git
    cd lab01-starter
    python -m venv .venv
    source .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    pip install -e .

  
## Run

Run the assistant from the terminal:

```bash
python -m assistant "where is the library?"
# -> Library: room B.201, open Mon-Sat 07:00-20:00.

python -m assistant "help"
# -> I can help you find university offices, their room numbers, and opening hours. Try asking 'Where is the Training Office?'

## Test

    pytest -q

## Troubleshooting

- "No module named assistant" -> you forgot `pip install -e .` or the venv is not active.
- PowerShell blocks Activate.ps1 -> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

## Evaluation / Benchmark

To run the benchmark evaluation script:

```bash
python eval/run.py
```
