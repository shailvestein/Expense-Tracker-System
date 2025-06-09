# Expense Tracker System

A simple and efficient Expense Tracker web application built using Python and Flask. This system allows users to track their daily expenses, categorize them, and view summaries for better financial management.

---

## Features

- Add, edit, and delete expenses
- Categorize expenses (e.g., Food, Transport, Utilities)
- View expense history with filters by date and category
- Dashboard summary with total expenses
- User-friendly and clean interface

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (or any other supported by SQLAlchemy)
- **Others:** Flask-WTF for forms, Flask-Login (if implemented for user authentication)

---

## Project Structure



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


---

## Installation

1. **Clone the repository:**

git clone https://github.com/shailvestein/Expense-Tracker-System.git
cd Expense-Tracker-System

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

python app.py

http://127.0.0.1:5000/

Usage
Use the dashboard to view all your expenses.

Add new expenses by clicking the "Add Expense" button.

Edit or delete any existing expense.

Filter expenses by date or category to analyze spending habits.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch: git checkout -b feature/your-feature-name

Make your changes and commit: git commit -m 'Add some feature'

Push to your branch: git push origin feature/your-feature-name

Open a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or feedback, reach out to:

Author: Shailesh Kumar Vishwakarma

Email: shailvestein.careers@gmail.com

GitHub: shailvestein

