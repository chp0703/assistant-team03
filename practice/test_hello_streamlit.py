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


def test_u2_greets_after_name_is_typed():
    at = run_app()
    assert len(at.success) == 0  # nothing typed yet -> no greeting
    at.text_input[0].input("An").run()
    assert at.success[0].value == "Hello, An!"


def test_u2_blank_name_shows_no_greeting():
    at = run_app()
    at.text_input[0].input("   ").run()
    assert len(at.success) == 0


def test_u3_counter_survives_reruns():
    at = run_app()
    assert "Clicked 0 times" in [m.value for m in at.markdown]
    at.button[0].click().run()
    at.button[0].click().run()
    assert "Clicked 2 times" in [m.value for m in at.markdown]


def test_u3_typing_does_not_reset_counter():
    at = run_app()
    at.button[0].click().run()
    at.text_input[0].input("An").run()  # another re-run, no click
    assert "Clicked 1 times" in [m.value for m in at.markdown]


def test_u4_default_load_is_normal():
    at = run_app()
    assert at.number_input[0].value == 18
    assert at.info[0].value == "18 credits is a normal load."
    assert len(at.error) == 0


def test_u4_boundary_30_is_still_normal():
    at = run_app()
    at.number_input[0].set_value(30).run()
    assert at.info[0].value == "30 credits is a normal load."
    assert len(at.error) == 0


def test_u4_more_than_30_needs_approval():
    at = run_app()
    at.number_input[0].set_value(31).run()
    assert at.error[0].value == "More than 30 credits needs advisor approval."
    assert len(at.info) == 0
