from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ============ DATABASE ============
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0,
        notes TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ============ USER ============
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user["id"], user["username"], user["password"])
    return None

# ============ ROUTES ============
@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username,password) VALUES (?,?)",
                         (username,password))
            conn.commit()
            flash("Compte créé !")
            return redirect(url_for("login"))
        except:
            flash("Utilisateur déjà existant")
        conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("dashboard"))
        flash("Identifiants incorrects")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    stats = conn.execute("SELECT wins,losses,draws FROM users WHERE id=?",
                         (current_user.id,)).fetchone()
    conn.close()
    return render_template("dashboard.html", stats=stats)

@app.route("/notes", methods=["GET","POST"])
@login_required
def notes():
    conn = get_db()
    if request.method == "POST":
        content = request.form["notes"]
        conn.execute("UPDATE users SET notes=? WHERE id=?",
                     (content,current_user.id))
        conn.commit()
    note = conn.execute("SELECT notes FROM users WHERE id=?",
                        (current_user.id,)).fetchone()
    conn.close()
    return render_template("notes.html", note=note["notes"] if note["notes"] else "")

@app.route("/cts")
@login_required
def cts():
    return render_template("cts.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
