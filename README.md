# Expense Tracker System

A simple, role-based expense tracker built with **Flask**, **Bootstrap**, and **PostgreSQL** (via Supabase), complete with admin login and CRUD functionality for managing expenses.

---

## 🚀 Features

- **Admin Authentication**: Secure login system using hashed passwords (via `werkzeug.security`).
- **Manage Expenses**: Add, view, edit, and delete expenses.
- **Contact & About Sections**: Admin-controlled content for about/contact info.
- **Skills, Education, Experience**: Dynamically update personal profile sections.
- **Live Data**: All content is stored in Supabase and rendered dynamically.
- **Responsive UI**: Mobile-first design powered by Bootstrap.

---

## 🧰 Tech Stack

- **Backend**: Python 3, Flask  
- **Frontend**: HTML5, CSS3, Bootstrap  
- **Database**: Supabase (PostgreSQL)  
- **Email**: Utility for sending emails (`send_mail.py`, optional)  
- **Deployment**: Compatible with Render, Heroku, or any Flask-capable service

---

## 📁 Project Structure

```
Expense-Tracker-System/
├── app.py # Main Flask app and route handlers
├── supabase_client.py # Supabase database client setup
├── send_mail.py # Optional email helper
├── requirements.txt # Python dependencies
├── static/ # Static files: CSS, JS, images
├── templates/ # Jinja2 HTML templates
│ ├── home.html
│ ├── login.html
│ ├── admin.html
│ ├── add.html
│ ├── edit.html
│ └── view.html
├── Procfile # For deployment (e.g. Heroku or Render)
└── README.md # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/shailvestein/Expense-Tracker-System.git
    cd Expense-Tracker-System
    ```

2. **Setup environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.template .env      # Create your secrets file
    # Add SUPABASE_URL, SUPABASE_KEY, SECRET_KEY, etc.
    ```

3. **Run the application:**
    ```bash
    python app.py
    ```
    Access via `http://localhost:5000`.

---

## 📝 Usage

- Visit `/login` to access admin dashboard.
- Use dashboard to **Add**, **Edit**, and **Delete** entries in:
  - Skills
  - Projects
  - Education
  - Experience
  - About
  - Contact
  - Expenses
- View dynamic content on the home page.

---

## 💬 Contributing

Contributions welcome! Suggested workflow:
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit your changes  
4. Open a pull request

---

## 📄 License

Open-sourced under the **MIT License** — check the LICENSE file for details.

---

## 🙏 Acknowledgments

Built using:
- Flask community  
- Bootstrap  
- Supabase  

---

Enjoy managing your expenses effortlessly! 😊  
— *Shailesh Kumar Vishwakarma*
