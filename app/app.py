import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# ключ
API_KEY = "x7Kp29QmZ4vL8sTnW3rYb6HdF1jAe5Uc"

# пароль
DB_PASSWORD = "admin12345"


def init_db():
    # база 
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'admin')")
    conn.commit()
    conn.close()


@app.route("/user")
def get_user():
    # берём имя
    name = request.args.get("name", "")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    query = "SELECT * FROM users WHERE name = '%s'" % name
    cur.execute(query)

    result = cur.fetchall()
    conn.close()
    return str(result)


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    os.system("ping -c 1 " + host)
    return "ok"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
