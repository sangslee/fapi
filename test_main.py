import base64
import pytest
from fastapi.testclient import TestClient
from main import app # Assuming your FastAPI app instance is named 'app' in main.py

# Fixture for TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Tests for /html endpoint
def test_html_plain_text(client: TestClient):
    response = client.get("/html?content=Hello, World!")
    assert response.status_code == 200
    assert response.text == "Hello, World!"
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_html_base64_encoded(client: TestClient):
    original_content = "<h1>This is a test</h1>"
    encoded_content_bytes = base64.b64encode(original_content.encode('utf-8'))
    encoded_content_str = encoded_content_bytes.decode('utf-8')
    
    response = client.get(f"/html?content={encoded_content_str}")
    assert response.status_code == 200
    assert response.text == original_content
    assert response.headers["content-type"] == "text/html; charset=utf-8"

# Tests for /encode endpoint
def test_encode_simple_string(client: TestClient):
    test_string = "Encode This String"
    expected_encoded_bytes = base64.b64encode(test_string.encode('utf-8'))
    expected_encoded_str = expected_encoded_bytes.decode('utf-8')
    
    response = client.get(f"/encode?data={test_string}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original"] == test_string
    assert json_response["encoded"] == expected_encoded_str

# Tests for /decode endpoint
def test_decode_valid_string(client: TestClient):
    original_string = "This was encoded"
    encoded_string_bytes = base64.b64encode(original_string.encode('utf-8'))
    encoded_string_str = encoded_string_bytes.decode('utf-8')
    
    response = client.get(f"/decode?data={encoded_string_str}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original_b64"] == encoded_string_str
    assert json_response["decoded"] == original_string

def test_decode_invalid_string(client: TestClient):
    invalid_base64_string = "This is not a valid base64 string %&*"
    response = client.get(f"/decode?data={invalid_base64_string}")
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["detail"] == "Invalid Base64 data"

def test_decode_invalid_padding(client: TestClient):
    # Valid Base64: "test", invalid: "test=" (padding error)
    # "test" -> "dGVzdA=="
    # Let's use a string that would cause padding issues if not handled
    problematic_b64_string = "dGVzdA" # "test" without padding
    
    # The endpoint should ideally handle strings that are valid *before* strict padding.
    # However, Python's base64.b64decode is strict about padding.
    # Let's test what happens if the server receives a string that python's b64decode would reject
    
    response = client.get(f"/decode?data={problematic_b64_string}")
    assert response.status_code == 400 # Expecting failure due to strict b64decode
    json_response = response.json()
    assert json_response["detail"] == "Invalid Base64 data"

def test_encode_empty_string(client: TestClient):
    test_string = ""
    expected_encoded_str = base64.b64encode(test_string.encode('utf-8')).decode('utf-8')
    
    response = client.get(f"/encode?data={test_string}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original"] == test_string
    assert json_response["encoded"] == expected_encoded_str

def test_decode_empty_string_encoded(client: TestClient):
    # Empty string "" encodes to "" in Base64
    encoded_string_str = "" # This is what b64encode("".encode()).decode() gives
    original_string = ""
    
    response = client.get(f"/decode?data={encoded_string_str}")
    # Depending on how base64.b64decode handles an empty string (it's valid)
    # Python's base64.b64decode("") returns b''
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original_b64"] == encoded_string_str
    assert json_response["decoded"] == original_string

def test_html_empty_content(client: TestClient):
    response = client.get("/html?content=")
    assert response.status_code == 200
    assert response.text == ""

def test_html_base64_encoded_empty_string(client: TestClient):
    original_content = ""
    encoded_content_str = base64.b64encode(original_content.encode('utf-8')).decode('utf-8') # Should be ""
    
    response = client.get(f"/html?content={encoded_content_str}")
    assert response.status_code == 200
    assert response.text == original_content
