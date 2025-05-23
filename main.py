import base64
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

import util

app = FastAPI()


@app.get("/")
async def root():
    """
    Provides a simple "Hello World" message.

    Returns:
        dict: A dictionary with a "message" key, which FastAPI converts
              to a JSONResponse. Example: {"message": "Hello World"}
    """
    return {"message": "Hello World"}


@app.get("/log")
async def log():
    """
    Returns a simple "OK" message.

    Often used for health checks or simple status indications.

    Returns:
        dict: A dictionary with a "message" key, which FastAPI converts
              to a JSONResponse. Example: {"message": "OK"}
    """
    return {"message": "OK"}


@app.get("/redirect")
async def redirector(
    url: Annotated[
        str, Query(description="The URL to redirect to. Can be Base64 encoded.")
    ] = "https://www.google.com"
):
    """
    Redirects the client to a specified URL.

    The provided URL can be plain or Base64 encoded. If encoded, it will be
    decoded before the redirection.

    Args:
        url (str): The URL to redirect to. Defaults to "https://www.google.com".
                   Can be Base64 encoded.

    Returns:
        RedirectResponse: A response that directs the client to the target URL.
    """
    if util.is_base64_encoded(url):
        decoded_bytes = base64.b64decode(url)
        url = decoded_bytes.decode('utf-8')
    return RedirectResponse(url)


@app.get("/sleep")
async def sleep(
    sec: Annotated[
        int,
        Query(
            description="Number of seconds to pause before returning an empty HTML page. Max 10 seconds."
        ),
    ] = 10
):
    """
    Pauses execution for a specified number of seconds, then returns an empty HTML page.

    The duration is capped at a maximum of 10 seconds.

    Args:
        sec (int): The number of seconds to pause. Defaults to 10.
                   Maximum value is 10.

    Returns:
        HTMLResponse: An empty HTML page, served after the specified delay.
    """
    if abs(sec) > 10:
        sec = 10
    body = '''
<!DOCTYPE html>
<head>
</head>
<body>
  <script>
    console.log("before");
    setTimeout(() => console.log("after"), {sec}000);
  </script>
</body>
</html>
    '''.format(sec=sec)
    return HTMLResponse(content=body, status_code=200)


@app.get("/html")
async def html_renderer(
    content: Annotated[str, Query(description="HTML content to render. Can be Base64 encoded.")]
):
    """
    Renders HTML content provided as a string.

    Args:
        content (str): The string content to be rendered as HTML.
                       If the string is Base64 encoded, it will be decoded first.

    Returns:
        HTMLResponse: An HTML response containing the provided content.
    """
    if util.is_base64_encoded(content):
        decoded_bytes = base64.b64decode(content)
        content = decoded_bytes.decode('utf-8')
    return HTMLResponse(content=content, status_code=200)


@app.get("/encode")
async def encode_data(
    data: Annotated[str, Query(description="String to be Base64 encoded.")]
):
    """
    Encodes the provided string data into Base64.

    Args:
        data (str): The string data to be Base64 encoded.

    Returns:
        JSONResponse: A JSON response containing the original data and its
                      Base64 encoded representation.
                      Example: {"original": "your_data", "encoded": "eW91cl9kYXRh"}
    """
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    encoded_data = encoded_bytes.decode('utf-8')
    return JSONResponse(content={"original": data, "encoded": encoded_data})


@app.get("/decode")
async def decode_data(
    data: Annotated[str, Query(description="Base64 encoded string to be decoded.")]
):
    """
    Decodes a Base64 encoded string.

    Args:
        data (str): The Base64 encoded string to be decoded.

    Returns:
        JSONResponse: A JSON response containing the original Base64 string
                      and its decoded representation if successful.
                      Example: {"original_b64": "eW91cl9kYXRh", "decoded": "your_data"}
    Raises:
        HTTPException: With status code 400 and detail "Invalid Base64 data"
                       if the input string is not valid Base64.
    """
    try:
        decoded_bytes = base64.b64decode(data.encode('utf-8'))
        decoded_data = decoded_bytes.decode('utf-8')
        return JSONResponse(content={"original_b64": data, "decoded": decoded_data})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 data")


@app.get("/document/write")
async def document_write(
    url: Annotated[
        str,
        Query(
            description="URL to fetch and write its content into the document via document.write()."
        ),
    ] = "http://localhost"
):
    """
    Fetches content from a specified URL and embeds it into an HTML page using document.write().

    Args:
        url (str): The URL from which to fetch content.
                   Defaults to "http://localhost".

    Returns:
        HTMLResponse: An HTML page containing a script that fetches content from the
                      provided URL and writes it to the document.
    """
    body = '''
<!DOCTYPE html>
<head>
</head>
<body>
  <script>
    var t = new XMLHttpRequest;
    t.onload = function () {{
      t.status >= 200 && t.status < 300 ? document.write(t.responseText) : console.error("Request failed with status: " + t.status)
    }};
    t.open("GET", "{url}");
    t.send();
  </script>
</body>
</html>
    '''.format(url=url)
    return HTMLResponse(content=body, status_code=200)
