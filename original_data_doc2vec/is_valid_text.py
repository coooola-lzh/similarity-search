from nltk.tokenize.util import is_cjk

def is_valid_text(s):
    """
    To check if the html text content is valid. We recognize a text content valid as if it contains any Japanese character.
    """
    return any([is_cjk(ch) for ch in s])

