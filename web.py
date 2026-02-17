from flask import Flask, redirect
from database import get_file

app = Flask(__name__)


@app.route("/watch/<code>")
def watch(code):
    file_id = get_file(code)
    if not file_id:
        return "Invalid link"

    return redirect(f"https://t.me/file/{file_id}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

