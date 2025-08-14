# Django Accounts & Posts Project

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

---

## 🧪 From scratch (how this project is made)

> These steps show **exactly how to build this project** from a fresh folder.

```bash
# 0) Make a project folder and enter it
mkdir django-accounts-posts && cd django-accounts-posts

# 1) Create & activate a virtualenv
python -m venv .venv
# Windows (PowerShell)
.\\.venv\\Scripts\\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 2) Install Django
pip install "Django>=5,<6"

# 3) Start a Django project (project name: config)
django-admin startproject config .

# 4) Start two apps: accounts and posts
python manage.py startapp accounts
python manage.py startapp posts
```

### 4.1 Add apps to `INSTALLED_APPS`
Edit `config/settings.py` and add:
```python
INSTALLED_APPS = [
    # Django defaults...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
    "accounts",
    "posts",
]
```

### 4.2 Project URLs
In `config/urls.py`, include app URLs:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("posts.urls")),  # posts as homepage
]
```

Create `accounts/urls.py` and `posts/urls.py` files.

### 4.3 Templates & static (recommended)
In `config/settings.py` ensure templates/static are configured:
```python
TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Create folders:
```
templates/
static/
```

---

## 👤 Accounts app (details)
Basic auth flows using Django’s built-in `User` model.

**URLs (suggested):**
- `/accounts/login/` – login view
- `/accounts/logout/` – logout view
- `/accounts/register/` – user sign-up
- `/accounts/profile/` – view/update profile (optional)

**Views (suggested):**
- Use `django.contrib.auth.views.LoginView/LogoutView`
- A simple `register` view to create users
- Optional `Profile` model linked to `User` via OneToOne for extra fields (bio, avatar)

**Templates (suggested):**
```
templates/accounts/login.html
templates/accounts/register.html
templates/accounts/profile.html
```

---

## 📝 Posts app (details)
Simple blog-style posts.

**Model (example):**
```python
# posts/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

**URLs (suggested):**
- `/` – list posts
- `/posts/<id>/` – post detail
- `/posts/create/` – create (login required)
- `/posts/<id>/update/` – update (author only)
- `/posts/<id>/delete/` – delete (author only)

**Views (suggested):**
- Use Django Class-Based Views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`)
- Add `LoginRequiredMixin` and per-object permissions to restrict edits to authors

**Templates (suggested):**
```
templates/posts/post_list.html
templates/posts/post_detail.html
templates/posts/post_form.html
templates/posts/post_confirm_delete.html
```

Run migrations after creating models:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ✅ Creating `requirements.txt`
In your activated virtualenv, install anything you need (Django, pillow if using images, etc.), then **freeze**:
```bash
pip freeze > requirements.txt
```

> Tip: run this any time you add/remove packages.

---

## 🗂 Recommended `.gitignore`
Use a Python/Django `.gitignore` (one is included in this repo).

---

## ☁️ Put it on GitHub

### Option A) With Git (recommended)
```bash
# 1) Initialize Git and commit
git init
git add .
git commit -m "Initial commit: Django accounts & posts"

# 2) Create an empty repo on GitHub (no README/.gitignore). Copy its URL.

# 3) Add remote & push
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

### Option B) Without Git (upload via web UI)
1. On GitHub, click **New repository** → name it → **Create**.  
2. Click **“uploading an existing file”**.  
3. Drag & drop your project folder contents (except the `.venv` folder).  
4. Add a commit message and **Commit changes**.

---

## 🔐 Environment variables (optional)
If you use secrets (email, 3rd-party keys), keep them out of Git. Example using `.env` (via [python-dotenv] or [django-environ]):
```
DEBUG=False
SECRET_KEY=replace-me
DATABASE_URL=sqlite:///db.sqlite3
```
Don’t commit `.env` — it’s ignored by `.gitignore`.

---

## 🧰 Common management commands
```bash
# Create admin user
python manage.py createsuperuser

# Collect static (when deploying)
python manage.py collectstatic
```

---

## 🧾 License
MIT (or choose your own).

---

## 🙋 Support
If you get stuck, open an issue in the repo or ask for help.
