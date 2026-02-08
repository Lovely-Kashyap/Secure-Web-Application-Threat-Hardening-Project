from flask import Flask, render_template_string, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Create database
conn = sqlite3.connect("users.db")
conn.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, email TEXT UNIQUE, password TEXT)")
conn.close()

# Design
style = """
<style>
body {
    background: #eaf3ff;  /* soft light blue background */
    font-family: Arial, Helvetica, sans-serif;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    color: #333;
}

.container {
    text-align: center;
}

.app-title {
    font-size: 34px;
    font-weight: bold;
    color: #1f4fa3;  /* main blue */
    margin-bottom: 8px;
}

.subtitle {
    font-size: 14px;
    color: #555;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 42px;
    border-radius: 14px;
    width: 420px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    border-top: 6px solid #1f4fa3;  /* blue accent */
}

h2 {
    margin-bottom: 18px;
    color: #1f4fa3;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 6px;
    border: 1px solid #c9dcff;
    font-size: 14px;
}

input:focus {
    outline: none;
    border: 1px solid #1f4fa3;
}

button {
    background: #1f4fa3;
    color: white;
    padding: 12px;
    width: 100%;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    margin-top: 10px;
}

button:hover {
    background: #163b7a;
}

a {
    display: block;
    margin-top: 15px;
    color: #1f4fa3;
    text-decoration: none;
    font-size: 14px;
}

.error {
    color: #d9534f;
    font-size: 13px;
    margin-top: 8px;
}
</style>
"""

# REGISTER
@app.route("/", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Input validation
        if len(username) < 3:
            error = "Username must be at least 3 characters"

        elif not email.endswith(".com") or "@" not in email or email.startswith("@"):
            error = "Enter a valid email (example: name@gmail.com)"

        elif len(password) < 8:
            error = "Password must be at least 8 characters long"

        elif not any(char.isdigit() for char in password):
            error = "Password must contain at least 1 number"

        elif not any(char.isupper() for char in password):
            error = "Password must contain at least 1 uppercase letter"
        else:
            conn = sqlite3.connect("users.db")

            # Check if email already exists
            existing = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

            if existing:
                error = "Email already registered"
            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                conn.execute("INSERT INTO users VALUES (?,?,?)", (username, email, hashed))
                conn.commit()
                conn.close()
                return redirect("/login")

            conn.close()

    return render_template_string(style + f"""
    <div class="container">
        <div class="app-title">Safe Sphere</div>
        <div class="subtitle">Secure Web Application & Threat Hardening Project</div>

        <div class="card">
            <h2>Create Account</h2>
            <form method="post">
                <input name="username" placeholder="Username" required>
                <input name="email" placeholder="Email" required>
                <input name="password" type="password" placeholder="Password" required>
                <button>Register</button>
            </form>
            <div class="error">{error}</div>
            <a href='/login'>Already have an account? Login</a>
        </div>
    </div>
    """)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    # Create attempt counter if not present
    if "attempts" not in session:
        session["attempts"] = 0

    if request.method == "POST":

        # Block login after 3 failed attempts
        if session["attempts"] >= 3:
            return render_template_string(style + """
            <div class="container">
                <div class="app-title">Safe Sphere</div>
                <div class="subtitle">Secure Web Application & Threat Hardening Project</div>

                <div class="card">
                    <h2>Access Blocked</h2>
                    <div class="error">Too many failed attempts. Try again later.</div>
                    <a href='/'>Back to Register</a>
                </div>
            </div>
            """)

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")

        # Check if input is email or username
        if "@" in username:
            user = conn.execute("SELECT * FROM users WHERE email=?", (username,)).fetchone()
        else:
            user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        conn.close()


        if user:
            if bcrypt.checkpw(password.encode(), user[2]):
                session["user"] = user[0]
                session["attempts"] = 0   # reset on success
                return redirect("/dashboard")

        session["attempts"] += 1
        error = f"Invalid login! Attempts left: {3 - session['attempts']}"
        return render_template_string(style + f"""
        <div class="container">
            <div class="app-title">Safe Sphere</div>
            <div class="subtitle">Secure Web Application & Threat Hardening Project</div>

            <div class="card">
                <h2>Login</h2>
                <form method="post">
                    <input name="username" placeholder="Username or Email" required>
                    <input name="password" type="password" placeholder="Password" required>
                    <button>Login</button>
                </form>

                <div class="error">{error}</div>

                <a href='/'>Create new account</a>
            </div>
        </div>
        """)

    return render_template_string(style + """
    <div class="container">
        <div class="app-title">Safe Sphere</div>
        <div class="subtitle">Secure Web Application & Threat Hardening Project</div>

        <div class="card">
            <h2>Login</h2>
            <form method="post">
                <input name="username" placeholder="Username or Email" required>
                <input name="password" type="password" placeholder="Password" required>
                <button>Login</button>
            </form>
            <a href='/'>Create new account</a>
        </div>
    </div>
    """)

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template_string(style + f"""
        <div class="container">
            <div class="app-title">Safe Sphere</div>
            <div class="subtitle">Authentication Successful</div>

            <div class="card">
                <h2>Welcome, {session['user']}</h2>
                <p>You are securely logged in.</p>
                <a href='/logout'><button>Logout</button></a>
            </div>
        </div>
        """)

    return redirect("/login")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

app.run(debug=True)