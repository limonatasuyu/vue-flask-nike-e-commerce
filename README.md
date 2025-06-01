# 🛍️ Simple E-Commerce App

A basic full-stack e-commerce catalog app built with **Flask**, **SQL (SQLite)**, and **Vue.js**. This project showcases product listings with category-based filtering, but does **not** include basket or purchasing features.

## ⚙️ Tech Stack

- **Frontend**: Vue 3 + Axios  
- **Backend**: Flask + Flask-CORS  
- **Database**: SQLite (via SQLAlchemy)  
- **API Format**: RESTful JSON

## ✨ Features

- Display all products
- Filter by category, price range, and search keyword
- View product details
- Fully responsive frontend
- No cart or payment — just catalog functionality

## 🚀 Getting Started

### Backend (Flask)

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
# Runs on http://localhost:5000
python main.py

```

### Frontend (Vue 3)

```bash
# Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Start the dev server
# Runs on http://localhost:8080
npm run serve

```
