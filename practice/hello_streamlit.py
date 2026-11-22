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

# U2 — react to input: text_input RETURNS what the user typed
st.header("U2 — React to input")
name = st.text_input("Your name")
if name.strip():
    st.success(f"Hello, {name.strip()}!")

# U3 — remember things with session_state.
# A normal variable (count = 0) would be reset on every re-run;
# st.session_state survives re-runs (one per browser tab).
st.header("U3 — Remember things")
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Click me"):
    st.session_state.count += 1
st.write(f"Clicked {st.session_state.count} times")

# U4 — validate input and give feedback the user can understand
st.header("U4 — Validate input")
credits = st.number_input(
    "Credits this semester", min_value=0, max_value=40, value=18, step=1
)
if credits > 30:
    st.error("More than 30 credits needs advisor approval.")
else:
    st.info(f"{credits} credits is a normal load.")
