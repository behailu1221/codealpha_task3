# codealpha_task3_secure_code_review
This review evaluates a small Flask-based web application containing user login, file upload, and template rendering functionality. The purpose is to identify security vulnerabilities, assess risks, and recommend secure coding practices..
Detailed Findings & Fixes

1.SQL Injection (Critical)
Location
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

Impact

An attacker can bypass authentication or dump/modify database.

Example attack

Input username:

admin' --


Password is ignored → login bypassed.

Fix

Use parameterized queries:

query = "SELECT * FROM users WHERE username=? AND password=?"
cur.execute(query, (username, password))

2.Hardcoded Secret Key (High)
Location
app.secret_key = "123456"

Impact

Predictable session tokens

Session hijacking possible

Fix

Use environment variable:

app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

3.SSTI (Server-Side Template Injection) (Critical)
Location
template = f"Hello {name}!"
return render_template_string(template)

Impact

An attacker could execute Python commands, e.g.:

http://localhost/greet?name={{7*7}}

Fix

Escape user input:

from markupsafe import escape
template = "Hello {{ name }}!"
return render_template_string(template, name=escape(name))

4.Insecure File Upload (Critical)
Location
file.save(os.path.join("uploads", file.filename))

Issues

No validation of filename

Allows uploading executable code

Directory traversal attack
Example:

file.filename = "../../app.py"

Fix

Use secure_filename:

from werkzeug.utils import secure_filename
filename = secure_filename(file.filename)


Also restrict file types.

5.Debug Mode Enabled (High)
Location
app.run(debug=True)

Impact

If exposed, attacker gets:

Full stack trace

Remote code execution (in older Werkzeug)

Fix

Disable in production:

app.run(debug=False)

6.Missing Password Hashing (High)

Passwords stored or compared as plaintext.

Fix

Use SHA-256 or bcrypt:

from werkzeug.security import check_password_hash

Severity Summary
Risk	Count
Critical	3
High	3
Medium	2

Final risk rating: CRITICAL
