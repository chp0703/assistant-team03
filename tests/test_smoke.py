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

def test_help():
    response = reply("help")
    assert "offices" in response
    assert "room numbers" in response
    assert "opening hours" in response
    
    
def test_help_case_insensitive():
    assert reply("HELP") == reply("help")
def test_partial_office_name():
    assert "I.101" in reply("where is training")


def test_partial_student_affairs():
    assert "I.102" in reply("where is student")
    
    
def test_partial_helpdesk():
    assert "E.005" in reply("where is helpdesk")
