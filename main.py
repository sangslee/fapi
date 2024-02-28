import base64

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

import util

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/log")
async def log():
    return {"message": "OK"}


@app.get("/redirect")
async def redirector(url: str = "https://www.google.com"):
    if util.is_base64_encoded(url):
        decoded_bytes = base64.b64decode(url)
        url = decoded_bytes.decode('utf-8')
    return RedirectResponse(url)


@app.get("/sleep")
async def sleep(sec: int = 10):
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


@app.get("/document/write", response_class=HTMLResponse)
async def document_write(url: str = "http://localhost"):
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
