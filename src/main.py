"""
MIT License

Copyright 2021-Present kal-byte

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import dotenv
import random
import string
from quart import Quart, request, redirect, send_file, Response
dotenv.load_dotenv()

app = Quart(__name__, static_url_path="/static", static_folder="/static")
app.secret_key = os.environ["SECRET_KEY"]


content_type_conv = {
    "image/png": ".png",
    "image/gif": ".gif",
    "image/jpeg": ".jpeg",
}


def generate_name() -> str:
    ret = random.choices(string.hexdigits, k=8)
    return "".join(ret)


@app.route("/")
async def index() -> str:
    return "Hi, welcome to my CDN. If you want the source to this contact kal#1806."


@app.route("/static/<name>")
async def get_static_file(name: str) -> Response:
    return await send_file("../static/" + name)


@app.route("/upload", methods=["POST"])
async def send_to_static() -> Response:
    token = request.args.get("token")

    if not token or token != app.secret_key:
        return "Invalid token provided in parameters.", 403

    files = await request.files
    file = files["file"]

    fmt = content_type_conv.get(file.content_type)
    full_name = generate_name() + fmt

    file.save("../static/" + full_name)
    return redirect("/static/" + full_name)


if __name__ == "__main__":
    app.run()
