#secure_app.py (Fixed Version)
from flask import Flask, request, render_template_string
import sqlite3
import os
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

app = Flask(__name__)

DATABASE = "users.db"

# ✔ Secure secret key
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return "Welcome to the Secure Health Portal"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()

        # ✔ Parameterized query
        query = "SELECT username, password FROM users WHERE username=?"
        user = cur.execute(query, (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            return f"Hello {escape(username)}, login successful!"
        return "Invalid login!"

    return """
        <form method="POST">
            <input name="username">
            <input name="password" type="password">
            <button>Login</button>
        </form>
    """

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    
    # ✔ Safe filename
    filename = secure_filename(file.filename)

    # ✔ File type restriction
    allowed = {"png", "jpg", "pdf"}
    if filename.split(".")[-1] not in allowed:
        return "File type not allowed", 400

    os.makedirs("uploads", exist_ok=True)
    file.save(os.path.join("uploads", filename))

    return "File uploaded safely!"

@app.route("/greet")
def greet():
    name = escape(request.args.get("name", "user"))

    # ✔ Prevent SSTI
    return render_template_string("Hello {{ name }}!", name=name)

if __name__ == "__main__":
    app.run(debug=False)
