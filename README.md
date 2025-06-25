# 🛒 Inventory Tracking App

A modern, responsive **Flask-based web app** to help students check live inventory across campus shops — saving time, avoiding unnecessary trips, and empowering students with real-time availability info.

This project is fully Dockerized and includes admin and user login presets for fast testing and demo. Ready to be extended for campus medical stores and student-powered product suggestions in future versions.

---

## 🚀 Features

- 🧾 **Live Inventory Dashboard** for all users
- 🔐 **Admin Panel** with:
  - Add/Edit/Delete inventory items
  - Rename products
  - Quick quantity update via ➕➖ buttons
  - Low-stock alert (items with quantity < 5 shown in red)
- 🔎 **Live Search Bar** on the inventory page
- 🌓 **Dark Mode** UI enabled
- 🧑‍🎓 Students can register as users (non-admin)
- ✨ Flask-WTF based form validations

---

## 🐳 Run with Docker

```bash
# Pull the latest image
docker pull asp117920/flask-app:latest

# Run the app
docker run -p 5000:5000 asp117920/flask-app:latest
```

---

## 👥 User Roles & Demo Credentials

| Role         | Username | Email              | Password |
|--------------|----------|--------------------|----------|
| Admin        | admin    | admin@example.com  | admin    |
| Normal User  | user     | user@example.com   | user     |

✅ **New users can register using the "Register" tab**  
👁️ **Only admins see admin controls (add/edit/low-stock)**

---

## 🎯 Use Case

> This project serves as a **digital representation of campus shop inventories**, allowing students to:

- View available products before physically visiting
- Avoid unnecessary trips if items are out of stock
- In the future version an option for adding new items based on student interest will also be added.
- Use the same app for campus **medical store inventory tracking** and **convenience store** which will be very helpful.

---

## 🧑‍💻 Tech Stack

- **Framework:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Forms & Auth:** Flask-WTF, Flask-Login
- **Styling:** Bootstrap 5 + custom CSS
- **Deployment Ready:** Dockerized

---

## ⚙️ Local Setup Without Docker

If you'd prefer to run the project manually without Docker, follow these steps:

```bash
# 1. Clone the Repository
git clone https://github.com/Asterisk18/inventory-app.git
cd inventory-app
```

# 2. Create a Virtual Environment
```python
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

# 3. Install Dependencies
```python
pip install -r requirements.txt
```

# 4. Set Up the Database
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

# 5. Run the App
```python
  python3 run.py
```

# App will be running at:
# http://localhost:5000
```
