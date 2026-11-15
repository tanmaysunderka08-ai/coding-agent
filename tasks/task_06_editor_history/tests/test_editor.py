from editor import Editor


def test_typing_and_undo():
    ed = Editor("hello")
    ed.type(5, " world")
    assert ed.text == "hello world"
    assert ed.undo() and ed.text == "hello"


def test_new_edit_clears_redo():
    ed = Editor("ab")
    ed.type(2, "c")
    ed.undo()
    ed.type(2, "d")
    assert ed.redo() is False and ed.text == "abd"


def test_history_limit():
    ed = Editor("", history_limit=2)
    for ch in "abc":
        ed.type(len(ed.text), ch)
    assert ed.undo() and ed.undo() and not ed.undo()
    assert ed.text == "a"


def test_erase_in_the_middle():
    ed = Editor("hello big world")
    ed.erase(5, 9)
    assert ed.text == "hello world"
    ed.undo()
    assert ed.text == "hello big world"


def test_erase_at_the_end():
    ed = Editor("hello world")
    ed.erase(5, 11)
    ed.undo()
    assert ed.text == "hello world"


def test_redo_after_undo():
    ed = Editor("abc")
    ed.erase(0, 1)
    ed.undo()
    ed.redo()
    assert ed.text == "bc"


def test_find_replace_round_trip():
    ed = Editor("the cat sat on the mat")
    assert ed.find_replace("cat", "dog")
    assert ed.text == "the dog sat on the mat"
    ed.undo()
    assert ed.text == "the cat sat on the mat"


def test_move_and_undo():
    ed = Editor("one two three")
    ed.move(0, 4, 13)
    assert ed.text == "two threeone "
    ed.undo()
    assert ed.text == "one two three"
