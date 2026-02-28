from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key" 

DB_NAME = "portfolio.db"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        email TEXT NOT NULL, 
        subject TEXT, 
        message TEXT NOT NULL, 
        date TEXT NOT NULL)''')
    
    # Chat logs table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_query TEXT NOT NULL, 
        bot_response TEXT NOT NULL, 
        timestamp TEXT NOT NULL)''')
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            first_name TEXT NOT NULL, 
            last_name TEXT NOT NULL, 
            email TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL, 
            role TEXT NOT NULL
        )''')
    
    # Create default Admin user if not exists
    c.execute("SELECT * FROM users WHERE email='admin@technova.com'")
    if not c.fetchone():
        c.execute("INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)", 
                  ('Admin', 'User', 'admin@technova.com', 'admin123', 'admin'))
        print("Admin created: admin@technova.com / admin123")
        
    conn.commit()
    conn.close()

init_db()

# --- DECORATORS FOR LOGIN ---
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to access this page.", "error")
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- ROUTES ---

@app.route("/")
def home():
    return render_template("index.html", user=session.get('first_name'))

@app.route("/portfolio")
def student_portfolio():
    return render_template("portfolio.html", user=session.get('first_name'))

# --- AUTHENTICATION ROUTES ---

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['first_name'] = user[1]
            session['email'] = user[3]
            session['role'] = user[5]
            flash(f"Welcome back, {user[1]}!", "success")
            if user[5] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", "error")
            
    return render_template("login.html", user=session.get('first_name'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)", 
                      (first_name, last_name, email, password, 'user'))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists.", "error")
        finally:
            conn.close()
            
    return render_template("register.html", user=session.get('first_name'))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

# --- ADMIN ROUTES ---

@app.route("/admin/dashboard")
@login_required(role='admin')
def admin_dashboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id ASC")
    messages = c.fetchall()
    
    # Also fetch chat logs for dashboard
    c.execute("SELECT * FROM chat_logs ORDER BY id ASC")
    chats = c.fetchall()
    
    conn.close()
    return render_template("admin_messages.html", messages=messages, chats=chats, user=session.get('first_name'))

# --- CONTACT & CHATBOT ---

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, email, subject, message, date) VALUES (?, ?, ?, ?, ?)",
              (name, email, subject, message, date))
    conn.commit()
    conn.close()
    flash("Your message has been sent successfully!", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    response = ""

    # --------- Rule-based Logic (Expanded) ----------
    if "hello" in user_message or "hi" in user_message:
        response = "Hello! Welcome to TechNova Solutions. How can I help you today?"
    elif "service" in user_message or "services" in user_message:
        response = ("We offer Web Development, UI/UX Design, Mobile App Development, "
                    "Digital Marketing, SEO, and Tech Consultancy. Check our Services section!")
    elif "contact" in user_message or "email" in user_message or "phone" in user_message:
        response = "You can contact us at manojyadav9027@gmail.com or call +91 9627587187."
    elif "timing" in user_message or "hours" in user_message or "open" in user_message:
        response = "Our office hours are Mon-Fri, 9:00 AM to 6:00 PM. Closed on weekends."
    elif "address" in user_message or "location" in user_message:
        response = "We are located at KNIT Sultanpur, UP, India."
    elif "project" in user_message or "portfolio" in user_message:
        response = ("We have completed many projects like E-Commerce sites, Coffee Shop websites, "
                    "and corporate websites. Check the Projects section!")
    elif "team" in user_message or "founder" in user_message:
        response = ("Our team consists of skilled developers and designers. "
                    "The founder is Manoj Yadav, leading TechNova Solutions with innovation.")
    elif "price" in user_message or "cost" in user_message or "charges" in user_message:
        response = ("Our pricing depends on project type, scope, and timeline. "
                    "Please contact us for a detailed quote.")
    elif "review" in user_message or "feedback" in user_message or "testimonial" in user_message:
        response = "We have many happy clients! Check our website for reviews and testimonials."
    elif "career" in user_message or "jobs" in user_message:
        response = ("TechNova Solutions occasionally hires developers, designers, and marketers. "
                    "Visit our Careers page for current openings.")
    elif "blog" in user_message or "articles" in user_message:
        response = "We regularly post articles and blogs on tech trends. Check our Blog section!"
    elif "privacy" in user_message or "policy" in user_message:
        response = "You can read our Privacy Policy and Terms on our website's footer section."
    elif "social" in user_message or "facebook" in user_message or "linkedin" in user_message:
        response = ("Follow us on social media: Facebook: fb.com/technovasolutions, "
                    "LinkedIn: linkedin.com/company/technovasolutions, "
                    "Instagram: instagram.com/technovasolutions")
    elif "faq" in user_message:
        response = ("You can check our FAQ section for common questions about services, pricing, "
                    "timings, and support.")
    elif "support" in user_message or "help" in user_message:
        response = ("For support, email manojyadav9027@gmail.com or call +91 9627587187. "
                    "We respond within 24 hours.")
    elif "software" in user_message or "app" in user_message:
        response = "We develop custom software and mobile applications tailored to your business needs."
    elif "training" in user_message or "workshop" in user_message:
        response = ("TechNova Solutions offers training sessions and workshops on web development, "
                    "digital marketing, and tech tools. Contact us for schedules.")
    elif "bye" in user_message or "exit" in user_message or "see you" in user_message:
        response = "Goodbye! Have a great day and feel free to reach out anytime."
    else:
        response = ("I am a simple bot. I can answer questions about our Services, Contact details, "
                    "Timings, Address, Projects, Team, Pricing, Reviews, Careers, Blogs, Policies, "
                    "Social Media, Support, Software, or Training.")

    # --------- Log chat to database ----------
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO chat_logs (user_query, bot_response, timestamp) VALUES (?, ?, ?)",
                  (user_message, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)