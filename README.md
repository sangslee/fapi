# FAPI - FastAPI Utility Service

A FastAPI-based web utility service that provides various web-related functionalities including URL redirection, HTML rendering, Base64 encoding/decoding, and content fetching.

## Features

- **URL Redirection**: Redirect to any URL with support for Base64-encoded URLs
- **HTML Rendering**: Render HTML content directly or from Base64-encoded strings
- **Base64 Operations**: Encode and decode strings to/from Base64
- **Content Fetching**: Fetch and render content from external URLs
- **Health Checks**: Simple health check endpoint
- **Sleep/Delay**: Configurable delay endpoint for testing purposes

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fapi
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Endpoints

### `GET /`
**Description**: Simple "Hello World" endpoint

**Response**:
```json
{
  "message": "Hello World"
}
```

### `GET /log`
**Description**: Health check endpoint

**Response**:
```json
{
  "message": "OK"
}
```

### `GET /redirect`
**Description**: Redirects to a specified URL

**Parameters**:
- `url` (query, optional): URL to redirect to. Can be Base64 encoded. Default: "https://www.google.com"

**Example**:
```bash
curl "http://localhost:8000/redirect?url=https://example.com"
```

### `GET /sleep`
**Description**: Pauses for specified seconds and returns an HTML page

**Parameters**:
- `sec` (query, optional): Number of seconds to pause (max 10). Default: 10

**Example**:
```bash
curl "http://localhost:8000/sleep?sec=5"
```

### `GET /html`
**Description**: Renders HTML content

**Parameters**:
- `content` (query, required): HTML content to render. Can be Base64 encoded.

**Example**:
```bash
curl "http://localhost:8000/html?content=<h1>Hello</h1>"
```

### `GET /encode`
**Description**: Encodes a string to Base64

**Parameters**:
- `data` (query, required): String to be Base64 encoded

**Response**:
```json
{
  "original": "your_data",
  "encoded": "eW91cl9kYXRh"
}
```

**Example**:
```bash
curl "http://localhost:8000/encode?data=Hello World"
```

### `GET /decode`
**Description**: Decodes a Base64 encoded string

**Parameters**:
- `data` (query, required): Base64 encoded string to decode

**Response**:
```json
{
  "original_b64": "SGVsbG8gV29ybGQ=",
  "decoded": "Hello World"
}
```

**Example**:
```bash
curl "http://localhost:8000/decode?data=SGVsbG8gV29ybGQ="
```

**Error Response** (400):
```json
{
  "detail": "Invalid Base64 data"
}
```

### `GET /document/write`
**Description**: Fetches content from a URL and embeds it using document.write()

**Parameters**:
- `url` (query, optional): URL to fetch content from. Default: "http://localhost"

**Example**:
```bash
curl "http://localhost:8000/document/write?url=https://api.example.com/data"
```

## Testing

Run the test suite using pytest:

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
pytest test_main.py -v
```

### Test Coverage

The test suite covers:
- HTML rendering with plain text and Base64 encoded content
- Base64 encoding and decoding operations
- Error handling for invalid Base64 data
- Edge cases (empty strings, invalid padding)

## Deployment

### Heroku

The project includes a `Procfile` for Heroku deployment:

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Deploy
git push heroku main
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fapi .
docker run -p 8000:8000 fapi
```

## Project Structure

```
fapi/
├── main.py           # Main FastAPI application
├── util.py           # Utility functions (Base64 validation)
├── test_main.py      # Test suite
├── requirements.txt  # Python dependencies
├── Procfile         # Heroku deployment configuration
└── README.md        # This file
```

## Dependencies

Key dependencies include:
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI web server implementation
- **Pydantic**: Data validation and settings management
- **pytest**: Testing framework (development)

See `requirements.txt` for the complete list of dependencies.
