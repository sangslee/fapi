import base64


def is_base64_encoded(input_string):
    try:
        # Attempt to decode the input string as Base64
        decoded_bytes = base64.b64decode(input_string)
        # If decoding is successful, it's a Base64-encoded string
        return True
    except Exception as e:
        # If an exception is raised, it's not Base64-encoded
        return False
