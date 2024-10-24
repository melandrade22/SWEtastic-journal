import data.text as txt


def test_read():
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str)


def test_read_one():
    assert len(txt.read_one(txt.TEST_KEY)) > 0


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}

def test_delete():
    # First, ensure the key exists before deleting
    assert txt.DEL_KEY in txt.read()

    # Delete the key and check that it was deleted
    delete_message = txt.delete(txt.DEL_KEY)
    assert delete_message == f"Deleted page with key: {txt.DEL_KEY}"
    assert txt.DEL_KEY not in txt.read()