"""Tests for the Lab 7 warm-up page, using Streamlit's AppTest (no browser)."""

from streamlit.testing.v1 import AppTest

APP = "hello_streamlit.py"  # resolved relative to this test file


def run_app() -> AppTest:
    at = AppTest.from_file(APP).run()
    assert not at.exception, at.exception
    return at


def test_u1_page_renders_title_and_text():
    at = run_app()
    assert at.title[0].value == "Hello, Streamlit 👋"
    assert "This page is written in Python only." in [m.value for m in at.markdown]
