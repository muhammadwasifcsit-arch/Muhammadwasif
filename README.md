Here’s a more **refined, professional, and detailed version** of your project README that makes everything clearer, well-structured, and more “portfolio-ready”:

---

# **TechNova Solutions Website**

A **Flask-based full-stack web application** serving as both a portfolio and organization website, featuring user authentication, interactive chatbot, and an admin dashboard for managing messages and logs.

---

## **Key Features**

* **Public Pages:**

  * Responsive **homepage** (`index.html`) showcasing the organization
  * **Student portfolio page** (`/portfolio`) displaying individual student projects

* **User Authentication:**

  * Register, login, and logout functionality
  * Role-based access control (users vs admin)

* **Contact System:**

  * Contact form submissions stored securely in **SQLite** database
  * Admins can view messages from the dashboard

* **Chatbot Module:**

  * Rule-based chatbot endpoint (`/chatbot`)
  * Chat history logged in `chat_logs` table for review

* **Admin Dashboard:**

  * View user messages and chatbot logs
  * Accessible only to users with admin privileges

---

## **Tech Stack**

* **Backend:** Python 3, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript

---

## **Project Structure**

```text
WebProject/
│-- app.py                # Main Flask application
│-- portfolio.db          # SQLite database
│-- static/
│   │-- style.css         # Main CSS
│   │-- script.js         # JavaScript functionality
│   └-- assets/           # Images, icons, and other assets
└-- templates/
    │-- index.html        # Homepage
    │-- portfolio.html    # Student portfolio page
    │-- login.html        # Login form
    │-- register.html     # Registration form
    └-- admin_messages.html # Admin dashboard for messages and logs
```

---

## **Database**

Database file: `portfolio.db`

Tables created automatically when the app starts:

| Table Name  | Purpose                                   |
| ----------- | ----------------------------------------- |
| `users`     | Stores user/admin credentials and roles   |
| `messages`  | Stores contact form submissions           |
| `chat_logs` | Stores chat interactions with the chatbot |

**Note:** `app.py` automatically creates a default admin if one does not exist.

**Default Admin Credentials (Local Development):**

* Email: `admin@technova.com`
* Password: `admin123`

> ⚠️ **Security Note:** Current setup stores passwords in plain text. For production, implement password hashing using `werkzeug.security` or similar.

---

## **Setup and Run**

1. **Create and activate virtual environment:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. **Install dependencies:**

```powershell
pip install flask
```

3. **Run the application:**

powershell
python app.py


4. **Open in your browser:**


http://127.0.0.1:5000/




## **Main Routes**

| Route              | Method   | Description                      |
| ------------------ | -------- | -------------------------------- |
| /                 | GET      | Homepage                         |
| /portfolio        | GET      | Student portfolio page           |
| /login            | GET/POST | Login page                       |
| /register         | GET/POST | Registration page                |
| /logout           | GET      | Logout                           |
| /submit_contact   | POST     | Contact form submission endpoint |
| /chatbot          | POST     | Chatbot interaction endpoint     |
| /admin/dashboard  | GET      | Admin dashboard (admin only)     |



## **Additional Notes**

Current `app.py` contains a duplicated chat logging block after `return jsonify(...)`. It is **unreachable** and can be safely removed for code cleanup.
* The application is **mobile-responsive** and designed for easy customization.
* Future improvements can include:

  * Password hashing and email verification
  * More advanced AI chatbot logic
  * Enhanced admin analytics dashboard



If you want, I can also **rewrite this README in a more “portfolio-style presentation”** with **eye-catching headers, badges, and short descriptions** so it looks perfect for GitHub or professional portfolios.

Do you want me to do that?
