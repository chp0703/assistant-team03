# Lab 7 — Streamlit warm-up (U1–U4)

A small practice page to learn Streamlit before working on the chat UI.

| Task | What it shows |
|------|---------------|
| U1 | a page written in Python only (`st.title`, `st.write`) |
| U2 | react to input (`st.text_input` → `st.success`) |
| U3 | remember values between re-runs (`st.session_state`) |
| U4 | validate input and give feedback (`st.number_input` → `st.error` / `st.info`) |

## Run

From the repository root, with the virtual environment active:

```bash
pip install -r practice/requirements.txt
streamlit run practice/hello_streamlit.py
# Local URL: http://localhost:8501
```

## Test

```bash
pytest -q practice/test_hello_streamlit.py
```

The tests use Streamlit's `AppTest`, which runs the page without a browser.
