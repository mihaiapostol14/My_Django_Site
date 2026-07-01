# 🚀 My Django Site
## Production-Ready Django 5.2 Portfolio Web Application

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/Django-5.2.8-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/mihaiapostol14/My_Django_Site?style=social)](https://github.com/mihaiapostol14/My_Django_Site)
[![Code Style: PEP 8](https://img.shields.io/badge/Code%20Style-PEP%208-blue.svg)](https://www.python.org/dev/peps/pep-0008/)

---

## 📖 Overview

**My Django Site** is a **production-ready** Django 5.2 portfolio web application demonstrating enterprise-grade development practices. The application implements a complete **email-based authentication system**, **custom user management**, and **responsive UI** with Bootstrap 5.2.3.

**Perfect for**: Prospective employers, code reviewers, and developers seeking a well-documented, maintainable Django foundation.

### 🎯 Key Highlights
- ✅ **Email-based authentication** (no usernames)
- ✅ **Custom User model** extending Django's AbstractUser
- ✅ **Image processing** with Pillow (auto-resizing to 300×300px)
- ✅ **Secure password hashing** via PBKDF2-SHA256
- ✅ **CSRF protection** on all forms
- ✅ **Responsive UI** with Bootstrap 5.2.3 + Font Awesome 6.3
- ✅ **SQLite3 dev** / PostgreSQL production-ready
- ✅ **Django ORM** with migrations

---

## 🏗️ Architecture & Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Framework** | Django MVT | 5.2.8 | Core web framework |
| **Language** | Python | 3.10+ | Backend runtime |
| **Database (Dev)** | SQLite3 | — | File-based development DB |
| **Database (Prod)** | PostgreSQL | 12+ | Production RDBMS |
| **ORM** | Django ORM | Native | Type-safe query layer |
| **Frontend** | Bootstrap | 5.2.3 | Responsive design system |
| **Icons** | Font Awesome | 6.3.0 | Vector icons |
| **Image Processing** | Pillow | 11.2.1 | Image optimization |
| **JavaScript** | Vanilla ES6+ | — | Client-side interactivity |
| **Session Backend** | Django Sessions | Native | Secure user sessions |
| **Authentication** | Custom User Model | Django Auth | Email-based login |

---

## 📂 Project Structure

```
My_Django_Site/
├── MyWebSite/                              # Django project root
│   ├── MyWebSite/                          # Project settings package
│   │   ├── settings.py                     # Django configuration (DB, APPS, SECURITY)
│   │   ├── urls.py                         # URL routing & namespacing
│   │   ├── wsgi.py                         # WSGI application entry point
│   │   ├── asgi.py                         # ASGI application entry point (async support)
│   │   └── __init__.py                     # Package marker
│   │
│   ├── authorization_user/                 # Authentication & user management app
│   │   ├── migrations/                     # Database schema version history
│   │   ├── models.py                       # CustomUser model (email-based, extends AbstractUser)
│   │   ├── views.py                        # Auth views (Registration, Login, Profile, Logout)
│   │   ├── forms.py                        # Form classes with Bootstrap styling
│   │   ├── urls.py                         # Auth-specific URL patterns
│   │   ├── utils.py                        # AuthorizationUserMixin for context injection
│   │   ├── admin.py                        # Django admin customization
│   │   └── apps.py                         # App configuration
│   │
│   ├── main/                               # Landing page & public content app
│   │   ├── migrations/                     # Database migrations
│   │   ├── models.py                       # Domain models
│   │   ├── views.py                        # HomeView (renders interactive calendar)
│   │   ├── urls.py                         # Public-facing URL patterns
│   │   ├── utils.py                        # HomeMixin for context enhancement
│   │   └── apps.py                         # App configuration
│   │
│   ├── templates/                          # Project-wide HTML templates
│   │   ├── base.html                       # Master template (navbar, footer, base layout)
│   │   ├── main/
│   │   │   └── home.html                   # Landing page with calendar widget
│   │   └── authentication_user/
│   │       ├── registration_user.html      # User registration form
│   │       ├── login_user.html             # Login form
│   │       ├── user_profile.html           # User profile display (auth required)
│   │       ├── change_password.html        # Password change form
│   │       └── logout_user.html            # Logout confirmation
│   │
│   ├── static/                             # Static assets (CSS, JS, images)
│   │   ├── css/                            # Custom stylesheets
│   │   ├── js/                             # JavaScript modules
│   │   └── images/                         # Static graphics & logos
│   │
│   ├── media/                              # User-uploaded files (demo only)
│   │   ├── user_photo/                     # User profile pictures
│   │   └── default_account_picture.jpg     # Default avatar fallback
│   │
│   ├── db.sqlite3                          # Development SQLite database
│   ├── manage.py                           # Django CLI management script
│   └── utils/                              # Shared application utilities
│
├── requirements.txt                        # Python dependencies manifest
├── README.md                               # This file
├── .gitignore                              # Version control exclusions
└── .env                                    # Environment variables (not in repo)
```

---

## 🔄 Runtime Architecture

### MVT (Model-View-Template) Flow
```
┌─────────────────────────────────────────────────────────────┐
│                     User HTTP Request                        │
│                    (GET /register | POST)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │   URL Router (urls.py)       │
          │ Dispatches to appropriate    │
          │        View Handler          │
          └────────────┬─────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────┐
        │  View (views.py)                     │
        │  • Form instantiation & validation   │
        │  • Business logic execution          │
        │  • Context data preparation          │
        └────────────┬─────────────────────────┘
                     │
                     ▼
      ┌─────────────────────────────────────────┐
      │  Model (models.py)                      │
      │  • ORM query execution                  │
      │  • Database interaction (SQLite/Postgres│
      │  • Data validation & constraints        │
      └────────────┬────────────────────────────┘
                   │
                   ▼
    ┌───────────────────────────────────────────────┐
    │  Template (templates/)                        │
    │  • HTML rendering with context data           │
    │  • Bootstrap UI components                    │
    │  • CSRF token & form rendering               │
    └────────────┬────────────────────────────────┘
                 │
                 ▼
    ┌───────────────────────────────────────────┐
    │  HTTP Response (HTML + Static Assets)    │
    │  Status: 200 | 302 | 404 | 500           │
    │  Headers: Set-Cookie (session), CSRF      │
    └───────────────────────────────────────────┘
```

### User Registration Flow (Detailed)
```
1. GET /authorization_user/registration-user/
   └─> CreateUserView renders form
       └─> User sees RegistrationUserForm (email, password, photo)

2. POST /authorization_user/registration-user/ (form submission)
   ├─> Form validation (email uniqueness, password strength)
   ├─> Custom save(): user.set_password() hashes via PBKDF2
   ├─> User instance persisted to database
   ├─> Auto-login via login(request, user, backend='ModelBackend')
   │   └─> session_id generated & stored in django_session table
   │   └─> session cookie set on response (HttpOnly, Secure in prod)
   └─> Redirect 302 to /authorization_user/user-profile/<pk>/

3. GET /authorization_user/user-profile/<pk>/
   ├─> UserDetailView fetches User instance
   ├─> Image validation & Pillow resizing (max 300×300px)
   ├─> Template renders profile with uploaded photo
   └─> HTTP 200 with user profile page
```

---

## 🔐 Authentication & Security

### Email-Based Authentication Strategy

```python
class User(AbstractUser):
    username = None                    # Username field removed
    email = models.EmailField(unique=True)  # PRIMARY_KEY for auth
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    photo = ImageField(...)
    
    USERNAME_FIELD = 'email'           # Django uses email for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']
```

**Why Email?**
- ✅ Universally unique (no collision disputes)
- ✅ Self-validates via RFC 5322
- ✅ Enables password recovery workflows
- ✅ Aligns with modern SaaS authentication standards
- ✅ No need for separate username management

### Security Features Implemented

| Feature | Status | Details |
|---------|--------|---------|
| **CSRF Protection** | ✅ | `{% csrf_token %}` on all forms |
| **Password Hashing** | ✅ | PBKDF2-SHA256 (Django default) with salt |
| **Email Validation** | ✅ | RFC 5322 compliant via `validate_email` |
| **File Upload Validation** | ✅ | JPG extension only via `FileExtensionValidator` |
| **Session Security** | ✅ | Django sessions with encrypted cookies |
| **Security Middleware** | ✅ | X-Frame-Options, XSS-Protection, CSRF middleware |
| **Image Processing** | ✅ | Pillow auto-resizes (prevents large file attacks) |

### ⚠️ Production Security Checklist

- [ ] **Move SECRET_KEY to `.env`** (currently hardcoded)
- [ ] **Set DEBUG=False** in production
- [ ] **Configure ALLOWED_HOSTS** for your domain
- [ ] **Enable HTTPS** via `SECURE_SSL_REDIRECT = True`
- [ ] **Set security headers**: `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- [ ] **Implement rate limiting** on `/authorization_user/login-user/` (e.g., `django-ratelimit`)
- [ ] **Add 2FA** via `django-otp` package
- [ ] **Implement email verification** on registration
- [ ] **Account lockout** after N failed login attempts
- [ ] **Upgrade password hashing** to Argon2 (via `django-argon2`)
- [ ] **Use PostgreSQL** instead of SQLite
- [ ] **Enable SECURE_BROWSER_XSS_FILTER** and **X-Content-Type-Options: nosniff**

---

## ⚡ Quick Start

### Prerequisites
- **Python**: 3.10+ ([Download](https://www.python.org/downloads/))
- **pip**: Package manager (included with Python 3.4+)
- **git**: Version control ([Download](https://git-scm.com/))

### Installation

```bash
git clone https://github.com/mihaiapostol14/My_Django_Site.git && cd My_Django_Site
```

### Environment Setup

#### 1️⃣ Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Verify activation (should show "(venv)" in prompt)
which python  # or "where python" on Windows
```

#### 2️⃣ Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 3️⃣ Navigate to Project Directory
```bash
cd MyWebSite
```

#### 4️⃣ Configure Environment Variables
Create `.env` file in `MyWebSite/` directory:
```bash
cat > .env << EOF
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for dev, PostgreSQL for prod)
DATABASE_URL=sqlite:///db.sqlite3

# Email (for password recovery)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EOF
```

#### 5️⃣ Apply Database Migrations
```bash
python manage.py migrate
```

#### 6️⃣ Create Superuser (Admin Account)
```bash
python manage.py createsuperuser

# Prompts:
# Email: admin@example.com
# First Name: Admin
# Last Name: User
# Password: (enter secure password)
# Password (again): (confirm)
```

#### 7️⃣ Run Development Server
```bash
python manage.py runserver

# Output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

#### 8️⃣ Access the Application
- **Home Page**: http://127.0.0.1:8000/
- **Register**: http://127.0.0.1:8000/authorization_user/registration-user/
- **Login**: http://127.0.0.1:8000/authorization_user/login-user/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (use superuser credentials)

---

## 🎨 Features

### 🔓 Authentication System
- ✅ **Email-based registration** with automatic login
- ✅ **Password hashing** via PBKDF2-SHA256
- ✅ **Secure login/logout** with session management
- ✅ **Password change** functionality
- ✅ **Profile customization** with photo upload
- ✅ **CSRF protection** on all forms

### 👤 User Profile Management
- ✅ **Custom User model** extending Django's AbstractUser
- ✅ **Profile photo upload** with validation (JPG only)
- ✅ **Automatic image resizing** (300×300px via Pillow)
- ✅ **Default profile picture** for users without uploads
- ✅ **User-specific profile display** (authentication required)

### 🏠 Home Page & Public Content
- ✅ **Interactive calendar widget** (renders current month)
- ✅ **Responsive navigation bar** with auth status
- ✅ **Bootstrap 5 UI** with Font Awesome icons
- ✅ **Public landing page** (no authentication required)

### 🛡️ Security & Admin
- ✅ **Django admin panel** with custom User admin
- ✅ **CSRF middleware** protecting all forms
- ✅ **Session-based authentication** with secure cookies
- ✅ **File extension validation** (prevents malicious uploads)
- ✅ **Email uniqueness enforcement** (prevents duplicate accounts)

### 📱 Responsive Design
- ✅ **Bootstrap 5.2.3** for mobile-first layout
- ✅ **Font Awesome 6.3** vector icons
- ✅ **Custom CSS** for theming (Grayscale template)
- ✅ **Vanilla JavaScript ES6+** for interactivity

---

## 🗄️ Database Management

### Development: SQLite3
```python
# settings.py (current)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

### Production: PostgreSQL

#### Step 1: Install PostgreSQL driver
```bash
pip install psycopg2-binary
```

#### Step 2: Update `settings.py`
```python
import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/mydjango_site'
)

db_from_env = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_from_env.path[1:],
        'USER': db_from_env.username,
        'PASSWORD': db_from_env.password,
        'HOST': db_from_env.hostname,
        'PORT': db_from_env.port or 5432,
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL
        },
    }
}
```

#### Step 3: Create PostgreSQL database
```bash
psql -U postgres

# Inside psql:
CREATE DATABASE mydjango_site;
CREATE USER myapp_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE mydjango_site TO myapp_user;
\q
```

#### Step 4: Migrate data
```bash
python manage.py migrate
python manage.py runserver
```

---

## 📊 Database Tables

| Table | Purpose |
|-------|---------|
| `authorization_user_user` | CustomUser model with profiles |
| `auth_group` | Permission groups (Django built-in) |
| `auth_permission` | Granular permissions |
| `django_session` | Active user sessions (encrypted) |
| `django_migrations` | Applied migration history |
| `django_admin_log` | Admin action audit trail |
| `django_content_type` | App registry metadata |

---

## 🔄 Database Migrations

### Create Migrations After Model Changes
```bash
python manage.py makemigrations authorization_user
python manage.py migrate
```

### View Migration History
```bash
python manage.py showmigrations
```

### Revert Migrations (Destructive!)
```bash
python manage.py migrate authorization_user 0001
```

### View Generated SQL
```bash
python manage.py sqlmigrate authorization_user 0002
```

---

## 🧪 Testing

### Run Unit Tests
```bash
cd MyWebSite
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test authorization_user
python manage.py test main
```

### Run with Verbose Output
```bash
python manage.py test --verbosity=2
```

---

## 🚀 Deployment

### Heroku Deployment
```bash
# 1. Install Heroku CLI
# 2. Create Procfile
cat > Procfile << EOF
web: gunicorn MyWebSite.wsgi
EOF

# 3. Create runtime.txt
echo "python-3.10.0" > runtime.txt

# 4. Update requirements.txt
pip freeze > requirements.txt

# 5. Deploy
heroku create your-app-name
heroku config:set SECRET_KEY='your-secret-key'
git push heroku main
heroku run python manage.py migrate
```

### Docker Deployment
```dockerfile
FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "MyWebSite.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
docker build -t my_django_site .
docker run -p 8000:8000 my_django_site
```

---

## 📝 Code Analysis & Quality Metrics

### PEP 8 Compliance
- ✅ Proper import ordering (stdlib → third-party → local)
- ✅ Descriptive variable & function names
- ✅ Class-based views following Django conventions
- ✅ Mixin patterns for code reuse

### Code Quality
- **Cyclomatic Complexity**: Low (simple views)
- **Type Coverage**: Partial (docstrings provided)
- **Test Coverage**: In progress

---

## 🤝 Contributing

Contributions are welcome! Please:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

---

## 📚 Documentation

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django User Authentication](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [Django Forms](https://docs.djangoproject.com/en/5.2/topics/forms/)
- [Pillow Image Processing](https://pillow.readthedocs.io/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.2/)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mihail Apostol**
- GitHub: [@mihaiapostol14](https://github.com/mihaiapostol14)
- Portfolio: [My Django Site](https://github.com/mihaiapostol14/My_Django_Site)

---

## 🙏 Acknowledgments

- **Django Community** for the excellent framework
- **Bootstrap** for responsive UI components
- **Font Awesome** for beautiful icons
- **Pillow** for image processing capabilities

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Open an [Issue](https://github.com/mihaiapostol14/My_Django_Site/issues)
- 🐛 Report a [Bug](https://github.com/mihaiapostol14/My_Django_Site/issues/new?template=bug_report.md)
- 💡 Request a [Feature](https://github.com/mihaiapostol14/My_Django_Site/issues/new?template=feature_request.md)

---

**⭐ If this project helped you, please consider giving it a star!**
