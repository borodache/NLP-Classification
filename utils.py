from re import sub

def clean_text(text):
    """
    Applies some pre-processing on the given text.

    Steps :
    - Lowering text
    - Removing backslashes
    - removes a. out of the answers
    - replaces 'b.', 'c.', and 'd.' with comma ','
    """
    text = text.lower()
    text = text.replace('\\', '')  # generic replace was advised by Danit
    text = text.replace('a.', '')
    text = text.replace('b.', ',')
    text = text.replace('c.', ',')
    text = text.replace('d.', ',')
    text = sub("\d+", "<num>", text)

    return ' '.join(text.split())
