# Django SocialHub Project

A clean, starter-friendly Django project with two apps: **accounts** and **posts**.  
This README includes **from-scratch instructions** (for learners) and **quickstart** steps (for running the repo).

---

## 📦 Tech Stack
- Python 3.11+
- Django 5.x
- SQLite (default) — easy to start; swap later for Postgres/MySQL if needed

---

## 🚀 Quickstart (running this repo)
> If you already have this code, follow these steps to run it locally.

```bash
# 1) Clone the repo (replace with your URL after you create it on GitHub)
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2) Create & activate a virtualenv
python -m venv .venv
# Windows (PowerShell)
.\\.venv\\Scripts\\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run migrations & create admin
python manage.py migrate
python manage.py createsuperuser

# 5) Start the dev server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## 🙋 Support
If you get stuck, open an issue in the repo or ask for help.
