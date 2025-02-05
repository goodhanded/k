'''
A utility module for counting tokens in a given text.
This is a simple approximation by splitting the text on whitespace.
'''

def count_tokens(text: str) -> int:
    """
    Approximates the token count of the given text by splitting on whitespace.

    Args:
        text (str): The text to count tokens for.

    Returns:
        int: The approximate number of tokens.
    """
    return len(text.split())
