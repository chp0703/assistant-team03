"""Lab 7 warm-up (U1–U4): Streamlit basics.

Run:   streamlit run practice/hello_streamlit.py
Test:  pytest -q practice/test_hello_streamlit.py

Streamlit re-runs this whole script from top to bottom on every interaction.
Each st.something(...) call draws one element on the page, in order.
"""

import streamlit as st

# U1 — a page written in Python only
st.title("Hello, Streamlit 👋")
st.write("This page is written in Python only.")
