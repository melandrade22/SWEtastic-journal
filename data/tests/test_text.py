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


def test_create():
    # Define a new key, title, and text for the new page
    new_key = 'NewPage'
    new_title = 'New Page Title'
    new_text = 'This is the content of the new page.'

    # Ensure the key does not exist before creating
    assert new_key not in txt.read()

    # Create the new page and check the message
    create_message = txt.create(new_key, new_title, new_text)
    assert create_message == f"Created page with key: {new_key}, title: {new_title}"

    # Ensure the key now exists and the content is correct
    created_page = txt.read_one(new_key)
    assert created_page[txt.TITLE] == new_title
    assert created_page[txt.TEXT] == new_text

    # Clean up by deleting the created page (optional for test consistency)
    txt.delete(new_key)


def test_delete():
    # First, ensure the key exists before deleting
    assert txt.DEL_KEY in txt.read()

    # Delete the key and check that it was deleted
    delete_message = txt.delete(txt.DEL_KEY)
    assert delete_message == f"Deleted page with key: {txt.DEL_KEY}"
    assert txt.DEL_KEY not in txt.read()


def test_update_text():
    assert txt.UPDATE_KEY in txt.read()
    msg = txt.update_text(txt.UPDATE_KEY, txt.UPDATE_TEST_VALUE)
    compare = f"Update page {txt.UPDATE_KEY} with text: {txt.UPDATE_TEST_VALUE}"
    assert msg == compare
    # Check that the changes persist
    assert txt.read()[txt.UPDATE_KEY][txt.TEXT] == txt.UPDATE_TEST_VALUE