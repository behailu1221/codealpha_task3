from flask import Flask, request, render_template_string, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = "users.db"

# ❌ Insecure: Hardcoded secret key
app.secret_key = "123456"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route("/")
def index():
    return "Welcome to the Health Portal"

# ❌ Insecure Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # ❌ SQL Injection Vulnerability
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        conn = get_db()
        cur = conn.cursor()
        result = cur.execute(query).fetchone()

        if result:
            return f"Hello {username}, login successful!"
        else:
            return "Invalid login!"
    return """
        <form method="POST">
            <input name="username">
            <input name="password" type="password">
            <button>Login</button>
        </form>
    """

# ❌ Vulnerable File Upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    # ❌ No file validation
    file.save(os.path.join("uploads", file.filename))

    return "File uploaded!"

# ❌ SSTI (Server-Side Template Injection)
@app.route("/greet")
def greet():
    name = request.args.get("name", "user")
    template = f"Hello {name}!"
    return render_template_string(template)

# ❌ Debug mode enabled
if __name__ == "__main__":
    app.run(debug=True)
