from flask import Flask, request, jsonify, redirect
import sqlite3
import random
import string

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            visits INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def generate_code():
    letters = string.ascii_letters + string.digits

    while True:
        code = ""

        for i in range(6):
            code += random.choice(letters)

        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT code FROM urls WHERE code = ?",
            (code,)
        )

        result = cursor.fetchone()
        conn.close()

        if result is None:
            return code


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if data is None or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    if not url.startswith("http://") and not url.startswith("https://"):
        return jsonify({"error": "Invalid URL"}), 400

    code = generate_code()
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO urls (url, code) VALUES (?, ?)",
        (url, code)
    )

    conn.commit()
    conn.close()

    short_url = request.host_url + code

    return jsonify({
        "url": url,
        "code": code,
        "short_url": short_url
    }), 201


@app.route("/<code>", methods=["GET"])
def redirect_url(code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT url FROM urls WHERE code = ?",
        (code,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return jsonify({"error": "Code not found"}), 404

    url = result[0]

    cursor.execute(
        "UPDATE urls SET visits = visits + 1 WHERE code = ?",
        (code,)
    )

    conn.commit()
    conn.close()

    return redirect(url)


@app.route("/<code>/stats", methods=["GET"])
def get_stats(code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT url, visits FROM urls WHERE code = ?",
        (code,)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "Code not found"}), 404

    url = result[0]
    visits = result[1]

    return jsonify({
        "url": url,
        "code": code,
        "visits": visits
    })


create_database()

if __name__ == "__main__":
    app.run(debug=True)
