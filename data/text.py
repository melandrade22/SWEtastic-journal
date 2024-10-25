"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
}


def create():
    pass


def delete(key: str) -> str:
    """
    Deletes a page by its key from the text_dict.
    If the key is not found, return a message indicating so.
    Args:
    key (str): The key for the page to delete.
    Returns:
        str: A message indicating the result of the deletion.
    """
    if key in text_dict:
        del text_dict[key]
        return f"Deleted page with key: {key}"
    else:
        return f"No page found with key: {key}"


# Function to update the text field of a specific key in the test dict
def update_text(key: str, val: str) -> str:
    """
    Update a page's text specified by its key with a new text value
    Args:
    key(str): The key for page to update
    val(str): The value to update the page key's TEXT field with
    Returns a string with message of success or not
    """
    if key in text_dict:
        text_dict[key][TEXT] = val
        return f"Updated page {key} with text: {val}"
    else:
        return f"No page found with key: {key}"


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Return an empty dictionary of key not found.
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def main():
    print(read())


if __name__ == '__main__':
    main()
