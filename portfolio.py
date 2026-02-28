
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages
DB_NAME = "portfolio.db"

# Function to create DB and messages table
def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

create_db()  # ensure table exists

# Home and other routes
@app.route("/")
@app.route("/about")
@app.route("/services")
@app.route("/projects")
@app.route("/contact")
def home():
    return render_template("index.html")  # Your single-page portfolio

# Contact form submission
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (name, email, subject, message, date) VALUES (?, ?, ?, ?, ?)",
        (name, email, subject, message, date),
    )
    conn.commit()
    conn.close()

    flash("Your message has been sent successfully!", "success")
    return redirect(url_for("home"))

# Admin route to view messages
@app.route("/admin/messages")
def view_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id ASC")
    messages = c.fetchall()
    conn.close()
    return render_template("admin_messages.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
