from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."


def test_hello_greeting():
    assert "Hello" in reply("hello")


def test_office_lookup_case_insensitive():
    assert "I.101" in reply("WHERE IS THE TRAINING OFFICE?")

def test_new_office_lookup():
    assert "A.201" in reply("Where is the Finance Office?")


def test_new_office_lookup_case_insensitive():
    assert "C.102" in reply("where is the international office?")

