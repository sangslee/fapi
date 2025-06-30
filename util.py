import base64
import binascii # Required for binascii.Error

def is_base64_encoded(input_string: str):
    """
    Checks if the input string is a valid Base64 encoded string.

    Args:
        input_string (str): The string to check.

    Returns:
        bool: True if the string is Base64 encoded, False otherwise.
    """
    if not input_string: # Handle empty string case explicitly if desired
        return False # Or True, depending on how empty string should be treated
                     # Python's b64decode treats empty string as valid, decodes to b''
                     # but often an empty string is not considered "encoded content"
    try:
        # Attempt to decode the input string (as UTF-8 bytes) as Base64
        # validate=True ensures stricter checking for padding and alphabet.
        base64.b64decode(input_string.encode('utf-8'), validate=True)
        return True
    except binascii.Error:
        # If a binascii.Error is raised, it's not a valid Base64-encoded string
        return False
    except UnicodeDecodeError:
        # If input_string itself is not valid something (e.g. not utf-8 representable bytes in a str)
        # This might be an edge case depending on how input_string is sourced.
        # For this function, we assume input_string should be convertible to utf-8 bytes.
        return False
