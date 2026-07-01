# My Django Site

## Executive Summary

**My Django Site** is a production-ready Django 5.2 portfolio web application demonstrating enterprise-grade development practices. The application implements a complete authentication system with email-based identity management, responsive UI with Bootstrap, and a scalable database architecture that supports transition from SQLite (development) to PostgreSQL (production).

**Target Audience**: Prospective employers, code reviewers, and developers seeking a well-documented, maintainable foundation for Django-based web applications.

**Repository Status**: 🟢 Public (Portfolio Demonstration) | ⚠️ Pre-Production (Development Database SQLite3)

---

## Architecture & Technology Stack

| Layer | Component | Technology | Version | Purpose |
|-------|-----------|-----------|---------|---------|
| **Framework** | Web Application | Django | 5.2.8 | Core MVT web framework |
| **Language** | Backend Runtime | Python | 3.10+ | Server-side logic & ORM |
| **Database** | RDBMS (Dev) | SQLite3 | — | File-based development database |
| **Database** | RDBMS (Prod) | PostgreSQL | 12+ | Recommended production-grade RDBMS |
| **ORM** | Object-Relational Mapping | Django ORM | Native | Type-safe query abstraction layer |
| **Frontend** | UI Framework | Bootstrap | 5.2.3 | Responsive, mobile-first design system |
| **Styling** | CSS Theme | Grayscale (Start Bootstrap) | Custom | Pre-built semantic design system |
| **Icons** | Icon Library | Font Awesome | 6.3.0 | Scalable vector icons |
| **JavaScript** | Client-side Logic | Vanilla JS | ES6+ | Interactive form validation, UX enhancement |
| **Image Processing** | Media Handling | Pillow | 11.2.1 | Dynamic image optimization & resizing |
| **Session Manager** | Session Backend | Django Sessions | Django | Secure, persistent user session management |
| **Authentication** | Auth System | Django Auth + Custom User Model | Django | Email-based authentication with permissions |
| **ASGI Support** | Async Support | asgiref | 3.8.1 | ASGI specification compliance |
| **SQL Utilities** | Query Parsing | sqlparse | 0.5.3 | SQL formatting & analysis |
| **Timezone DB** | Localization | tzdata | 2025.2 | Authoritative IANA timezone database |

---

## Project Organization

```
My_Django_Site/
├── MyWebSite/                          # Django project root
│   ├── MyWebSite/                      # Project settings package
│   │   ├── settings.py                 # Django configuration (SECRET_KEY, DB, APPS)
│   │   ├── urls.py                     # URL routing configuration
│   │   ├── wsgi.py                     # WSGI application entry point
│   │   ├── asgi.py                     # ASGI application entry point
│   │   └── __init__.py
│   │
│   ├── authorization_user/             # Authentication & user management app
│   │   ├── migrations/                 # Database schema version history
│   │   ├── models.py                   # User model (CustomUser extending AbstractUser)
│   │   ├── views.py                    # Auth views (Registration, Login, Profile, Logout)
│   │   ├── forms.py                    # Form classes (Registration, Login, PasswordChange)
│   │   ├── urls.py                     # Auth-specific URL patterns
│   │   ├── utils.py                    # AuthorizationUserMixin for context injection
│   │   ├── admin.py                    # Admin panel customization
│   │   └── apps.py                     # App configuration
│   │
│   ├── main/                           # Landing page & public content app
│   │   ├── migrations/                 # Database schema version history
│   │   ├── models.py                   # Domain models (if any)
│   │   ├── views.py                    # HomeView (renders calendar)
│   │   ├── urls.py                     # Public-facing URL patterns
│   │   ├── utils.py                    # HomeMixin for context enhancement
│   │   └── apps.py                     # App configuration
│   │
│   ├── templates/                      # Project-wide templates
│   │   ├── base.html                   # Master template with navbar, footer
│   │   ├── main/
│   │   │   └── home.html               # Landing page with calendar widget
│   │   └── authentication_user/
│   │       ├── registration_user.html  # User registration form
│   │       ├── login_user.html         # Login form
│   │       ├── user_profile.html       # User profile display (auth required)
│   │       ├── change_password.html    # Password change form
│   │       └── logout_user.html        # Logout confirmation
│   │
│   ├── static/                         # Static assets (CSS, JS, images)
│   │   ├── css/                        # Stylesheets
│   │   ├── js/                         # JavaScript bundles
│   │   └── images/                     # Static graphics
│   │
│   ├── media/                          # User-uploaded files (dev/demo only)
│   │   ├── user_photo/                 # User profile pictures
│   │   └── default_account_picture.jpg # Fallback profile picture
│   │
│   ├── db.sqlite3                      # Development database (not for production)
│   ├── manage.py                       # Django management CLI
│   └── utils/                          # Shared application utilities
│
├── requirements.txt                    # Python dependency manifest
├── README.md                           # This file
└── .gitignore                          # Version control exclusions
```

## Runtime Architecture

The application follows Django's **Model-View-Template (MVT)** pattern:

```
User Request
    ↓
URL Router (urls.py) → Dispatches to appropriate View
    ↓
View (views.py) → Processes business logic, fetches data
    ↓
Model (models.py) → Queries database via ORM
    ↓
Template (templates/) → Renders HTML with context data
    ↓
HTTP Response (HTML + Static Assets)
```

### Key Request Flow: User Registration

1. User navigates to `/authorization_user/registration-user/`
2. `CreateUserView` (CBV) renders `registration_user.html` with form
3. Form submission → `RegistrationUserForm.save()` → `User` model instance created
4. `set_password()` hashes plaintext password via PBKDF2
5. Auto-login via `login()` function creates session
6. Redirect to `/authorization_user/user-profile/<id>`
7. `UserDetailView` displays profile with uploaded photo (auto-resized to 300×300px via Pillow)

---

## Authentication & Identity System

### Primary Identifier Strategy

**Current Implementation**: **Email-based** (username field removed from model)

```python
class User(AbstractUser):
    username = None  # Explicitly removed; email is PRIMARY_KEY
    email = models.EmailField(unique=True, validators=[validate_email])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='user_photo', default='default_account_picture.jpg')
    
    USERNAME_FIELD = 'email'  # Auth identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
```

**Why Email?**
- Universally unique across users
- Self-validates via RFC 5322
- No username collision disputes
- Aligns with modern SaaS standards
- Enables password recovery workflows

### Authentication Pipeline

```mermaid
graph TD
    A["User Visits /authorization_user/registration-user/"] -->|GET| B["CreateUserView<br/>renders form"]
    B --> C["RegistrationUserForm<br/>(email, password, photo)"]
    C --> D["User submits form<br/>POST request"]
    D --> E{Form Valid?}
    E -->|No| F["Render form with<br/>validation errors"]
    F --> C
    E -->|Yes| G["Hash password<br/>via set_password"]
    G --> H["Save User instance<br/>to database"]
    H --> I["Auto-login user<br/>login function"]
    I --> J["Create session_id<br/>in django_session table"]
    J --> K["Set session cookie<br/>in response"]
    K --> L["Redirect to<br/>/user-profile/pk"]
    
    M["User Visits /authorization_user/login-user/"] -->|GET| N["LoginUserView<br/>renders form"]
    N --> O["LoginUserForm<br/>(email, password)"]
    O --> P["User submits credentials<br/>POST request"]
    P --> Q{Email exists?}
    Q -->|No| R["Render login error"]
    R --> O
    Q -->|Yes| S{Password match?}
    S -->|No| R
    S -->|Yes| T["Authenticate via<br/>ModelBackend"]
    T --> U["Create session_id"]
    U --> V["Set session cookie"]
    V --> W["Redirect to /user-profile/pk"]
    
    X["User Clicks Logout"] -->|GET/POST| Y["UserLogoutView"]
    Y --> Z["Call logout request"]
    Z --> AA["Flush session<br/>from database"]
    AA --> AB["Delete session<br/>cookie"]
    AB --> AC["Redirect to home"]
```

### Form Validation & Field Constraints

| Field | Validator | Constraints | Purpose |
|-------|-----------|-------------|---------|
| **email** | `validate_email` (RFC 5322) | Max 254 chars, unique | Prevents duplicate accounts; RFC-compliant |
| **first_name** | Django CharField | 4-50 chars, non-empty | User identification |
| **last_name** | Django CharField | 4-50 chars, non-empty | User identification |
| **password** | `set_password()` + validators | 5-8 chars | PBKDF2 hashed (default Django backend) |
| **photo** | `FileExtensionValidator` | JPG only | Security: prevents malicious uploads |

### Security Implementation

✅ **Implemented**:
- ✓ CSRF protection via `{% csrf_token %}` on all forms
- ✓ Password hashing via PBKDF2-SHA256 (Django default)
- ✓ Session-based authentication with HttpOnly cookies
- ✓ File extension validation (JPG images only)
- ✓ HTTP security middleware (X-Frame-Options, XSS-Protection headers)
- ✓ User permission framework (Django's `PermissionsMixin`)
- ✓ Automatic image optimization (Pillow, max 300×300px)

⚠️ **Recommendations for Production**:
- [ ] Implement rate limiting on `/authorization_user/login-user/` (e.g., `django-ratelimit`)
- [ ] Add two-factor authentication (2FA) via `django-otp`
- [ ] Implement email verification on registration
- [ ] Add account lockout after N failed login attempts
- [ ] Use stronger password hashing: Argon2 (via `django-argon2`)
- [ ] Implement HTTPS enforcement via `SECURE_SSL_REDIRECT = True`
- [ ] Enable security headers: `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`

---

## Database Management

### Current Strategy: SQLite3 (Development)

**Why SQLite?**
- Zero configuration, file-based database
- Perfect for local development and prototyping
- No external server or service dependencies
- Sufficient for portfolio demonstration
- Django migrations handle schema versioning

**Location**: `MyWebSite/db.sqlite3` (in project root)

**Current Configuration** (from `settings.py`):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

**Database Tables** (created via `python manage.py migrate`):
- `authorization_user_user` — CustomUser model with all profile data
- `auth_group` — Permission groups (Django built-in)
- `auth_permission` — Granular permissions (Django built-in)
- `django_session` — Active user sessions (encrypted)
- `django_migrations` — Applied migration history
- `django_admin_log` — Admin action audit trail
- `django_content_type` — App registry metadata

### Production Migration: PostgreSQL

SQLite is **not recommended for production**. Follow these steps to migrate to PostgreSQL:

#### Step 1: Install PostgreSQL Client Library
```bash
# For production deployments
pip install psycopg2-binary

# For local development (requires system PostgreSQL development headers)
pip install psycopg2
```

#### Step 2: Update `settings.py` to Use Environment Variables
```python
import os
from urllib.parse import urlparse

# Use DATABASE_URL environment variable (supports heroku-style URLs)
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/mydjango_site'
)

# Parse connection string
db_from_env = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_from_env.path[1:],  # Remove leading '/' from path
        'USER': db_from_env.username,
        'PASSWORD': db_from_env.password,
        'HOST': db_from_env.hostname,
        'PORT': db_from_env.port or 5432,
        'CONN_MAX_AGE': 600,  # Connection pooling: 10 minutes
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL in production
        },
    }
}
```

#### Step 3: Create PostgreSQL Database & User
```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Inside psql:
CREATE DATABASE mydjango_site;
CREATE USER myapp_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE mydjango_site TO myapp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO myapp_user;
\q
```

#### Step 4: Migrate Existing Data (If Any)
```bash
# Export data from SQLite
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json

# Update DATABASES in settings.py to point to PostgreSQL
# Then apply migrations:
python manage.py migrate

# Load exported data:
python manage.py loaddata data.json
```

#### Step 5: Verify PostgreSQL Connection
```bash
# Should drop you into PostgreSQL shell (psql)
python manage.py dbshell

# List tables:
\dt

# Exit:
\q

# Run tests to ensure data integrity:
python manage.py test
```

### Media File Strategy

**Current Structure**:
```
media/
├── user_photo/                 # User-uploaded profile pictures
└── default_account_picture.jpg # Fallback default avatar
```

#### Why Media Files Are Included in This Repository

This is an **educational portfolio repository**. The media files demonstrate the complete working application. They show:
- File upload validation in action
- Image processing pipeline (Pillow resizing)
- User profile pictures on the detail page

#### Production Best Practices

In production, media files **SHOULD NOT** be in version control. Use external cloud storage:

**Updated `.gitignore` for production**:
```bash
media/
!media/.gitkeep             # Keep directory structure
staticfiles/                # Collected static files (generated)
*.sqlite3                   # Database (never commit)
.env                        # Environment secrets
.venv/
__pycache__/
*.pyc
```

**Why Remove Media from Git**:
1. **Bloats repository** — Images increase clone size significantly
2. **Scalability** — External storage (S3, GCS) handles distribution
3. **Security** — User-uploaded files should not be versioned
4. **Compliance** — GDPR requires deletion capability; Git history is immutable

**Production Media Handling via AWS S3**:
```bash
# Install django-storages
pip install django-storages boto3
```

```python
# settings.py (production only, use environment variables)
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

DEFAULT_FILE_STORAGE = 'path.to.MediaStorage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

### Data Migrations & Schema Evolution

#### Creating Migrations After Model Changes
```bash
# After modifying a model in authorization_user/models.py
python manage.py makemigrations authorization_user

# Apply the migration to database
python manage.py migrate

# Example output:
# Migrations for 'authorization_user':
#   0001_initial.py
#     - Create model User
#   0002_add_photo_field.py
#     - Add field photo to user
```

#### Viewing Migration History
```bash
python manage.py showmigrations

# Output:
# admin
#  [X] 0001_initial
#  [X] 0002_logentry options
# auth
#  [X] 0001_initial
#  [X] 0002_alter user options
# authorization_user
#  [X] 0001_initial
#  [X] 0002_add_photo_field
```

#### Reverting Migrations (Destructive)
```bash
# Revert to specific migration
python manage.py migrate authorization_user 0001

# This will rollback 0002_add_photo_field and delete the 'photo' column
```

#### Viewing SQL Generated by Migrations
```bash
python manage.py sqlmigrate authorization_user 0002
```

---

## Setup & Configuration

### Prerequisites

- **Python**: 3.10+ ([Download](https://www.python.org/downloads/))
- **pip**: Package manager (included with Python 3.4+)
- **git**: Version control ([Download](https://git-scm.com/))
- **virtualenv** or **venv**: Virtual environment isolation (recommended)
- **PostgreSQL** (optional, for production): [Download](https://www.postgresql.org/download/)

### Environment Initialization

#### 1. Clone Repository
```bash
git clone https://github.com/mihaiapostol14/My_Django_Site.git
cd My_Django_Site
```

#### 2. Create Virtual Environment
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

# Verify activation (your prompt should show "(venv)")
which python  # or "where python" on Windows
```

#### 3. Upgrade pip & Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 4. Navigate to Django Project Directory
```bash
cd MyWebSite
```

#### 5. Environment Configuration (.env)

Create a `.env` file for development:

```bash
# .env (Development)
DEBUG=True
SECRET_KEY='django-insecure-your-development-key-here'
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (use SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email (optional - uses console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**For Production** (use `python-decouple` for type-safe config):
```bash
pip install python-decouple
```

Update `settings.py`:
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')  # Raises error if missing
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
DATABASE_URL = config('DATABASE_URL')
```

**IMPORTANT**: Add `.env` to `.gitignore` to prevent committing secrets.

#### 6. Initialize Database
```bash
python manage.py migrate

# Expected output:
# Operations to perform:
#   Apply all migrations: admin, auth, authorization_user, contenttypes, main, sessions
# Running migrations:
#   Applying admin.0001_initial... OK
#   Applying admin.0002_logentry_remove_auto_add... OK
#   ...
#   Applying sessions.0001_initial... OK
```

#### 7. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser

# Interactive prompts:
# Email: admin@example.com
# First name: John
# Last name: Doe
# Password: ••••••••••
# Password (again): ••••••••••
# Superuser created successfully.
```

#### 8. Collect Static Files (Production Only)
```bash
python manage.py collectstatic --noinput

# Output:
# 1234 static files copied to '/path/to/staticfiles/', 0 unmodified, 0 post-processed.
```

#### 9. Run Development Server
```bash
python manage.py runserver

# Output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

#### 10. Access Application
- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (use superuser credentials)
- **Register User**: http://127.0.0.1:8000/authorization_user/registration-user/
- **Login**: http://127.0.0.1:8000/authorization_user/login-user/

### Secret Management

#### ⚠️ Security Warning

The repository **intentionally exposes** `SECRET_KEY` in `settings.py` for demonstration purposes. This is **NOT** acceptable in production.

**Production Secret Checklist**:
- ✅ Move `SECRET_KEY` to environment variable (`.env` or secrets manager)
- ✅ Add `.env` to `.gitignore`
- ✅ Use cryptographically strong secrets (40+ characters)
- ✅ Rotate secrets periodically (minimum: quarterly)
- ✅ Use separate secrets for development/staging/production
- ✅ Never commit or share secrets in pull requests

#### Generating a Secure Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Output example:
# a3!v0@v%n-4m^&e$5&v=z^!h-_m0#v6@2a+bj&^=zk!&v$4&k
```

---

## Administrative Operations

### Superuser Management

#### Create Superuser
```bash
python manage.py createsuperuser

# Follow interactive prompts
```

#### Change Superuser Password
```bash
python manage.py changepassword admin
# Follow prompts to enter new password
```

#### Delete User (Admin or Regular)
```bash
python manage.py shell

# In the Python shell:
>>> from authorization_user.models import User
>>> user = User.objects.get(email='user@example.com')
>>> user.delete()
(1, {'authorization_user.User': 1})  # Confirmation
>>> exit()
```

#### List All Users with Admin Status
```bash
python manage.py shell

# In the Python shell:
>>> from authorization_user.models import User
>>> users = User.objects.all()
>>> for user in users:
...     print(f"{user.email} ({user.first_name} {user.last_name}) - Admin: {user.is_staff}")
>>> exit()
```

### Admin Panel Features

Access at: http://127.0.0.1:8000/admin/

**Capabilities**:
- ✓ Create, edit, delete users
- ✓ Manage permissions and groups
- ✓ View login history (via `django_admin_log`)
- ✓ Configure site-level settings
- ✓ Monitor authentication attempts
- ✓ Bulk user operations

### Custom Management Commands

You can create custom Django management commands for common tasks:

**Example**: Create a command to generate test data:

```python
# File: MyWebSite/authorization_user/management/commands/create_test_users.py
from django.core.management.base import BaseCommand
from authorization_user.models import User

class Command(BaseCommand):
    help = 'Create test users for development'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of test users to create'
        )
    
    def handle(self, *args, **options):
        count = options['count']
        for i in range(1, count + 1):
            User.objects.create_user(
                email=f'testuser{i}@example.com',
                first_name=f'Test{i}',
                last_name='User',
                password='TestPass123'
            )
        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {count} test users')
        )
```

**Run the command**:
```bash
python manage.py create_test_users --count 10
```

---

## Repository Integrity & Security Philosophy

### Public Repository Rationale

**Why This Repository is Public**:

1. **Portfolio Demonstration** — Showcases Django development expertise for potential employers
2. **Educational Reference** — Serves as a reference implementation for:
   - Custom user model architecture
   - Authentication workflow design
   - Database migration strategy
   - Form validation patterns
3. **Open Source Philosophy** — Encourages community feedback, contributions, and learning
4. **Code Review Ready** — Structured and documented for senior code review and critique

### Security Practices Implemented

✅ **Security In Place**:
- ✓ CSRF tokens on all forms
- ✓ Password hashing via PBKDF2-SHA256
- ✓ Session-based authentication with HTTPOnly cookies
- ✓ File upload validation (extension + type checking)
- ✓ HTTP security middleware enabled
- ✓ Django permission framework integrated

⚠️ **Intentional Exposures** (for demonstration purposes):
- `SECRET_KEY` in source code (should use `.env` in production)
- `DEBUG=True` in `settings.py` (should be False in production)
- `ALLOWED_HOSTS=[]` (too permissive, restrict in production)
- Media files committed (should use cloud storage in production)
- SQLite database included (should use PostgreSQL in production)

These exposures are **intentional** to show a complete, working application. Production deployments must follow the documented best practices above.

### What's Excluded (Proper Security)

The repository **correctly excludes** (via `.gitignore` equivalent):
- Environment secrets (`.env`)
- Database files in production
- Sensitive configuration
- API keys and tokens
- User-generated media in production scenarios

---

## Views & Logic Layer (MVT Pattern)

### URL Routing Overview

```
Main App (main.urls):
  /                                    → HomeView (displays calendar)
  /<int:year>/<str:month>             → HomeView (dynamic calendar)

Authorization App (authorization_user.urls):
  /authorization_user/registration-user/  → CreateUserView (GET: form, POST: register)
  /authorization_user/login-user/         → LoginUserView (GET: form, POST: auth)
  /authorization_user/user-profile/<pk>   → UserDetailView (authenticated only)
  /authorization_user/change-password/    → ChangeUserPasswordView (authenticated)
  /authorization_user/logout-user/        → UserLogoutView (POST: logout)
```

### View Implementations

#### HomeView (main/views.py)
```python
class HomeView(HomeMixin, TemplateView):
    """
    Public landing page with calendar widget.
    
    Query Parameters:
        year (int, optional): Year for calendar (default: current year)
        month (str, optional): Month name (default: current month)
    
    Context:
        calendar_object: HTML-rendered calendar
        title: Page title
    """
    template_name = 'main/home.html'
    
    def put_calendar(year, month):
        """Generate HTML calendar for given month/year"""
        # Returns formatted HTML table via HTMLCalendar
```

#### CreateUserView (authorization_user/views.py)
```python
class CreateUserView(CreateView, AuthorizationUserMixin):
    """
    User registration endpoint.
    
    GET: Render registration form (RegistrationUserForm)
    POST: Validate form, create user, auto-login, redirect to profile
    
    Form fields:
        - first_name (required, 4-50 chars)
        - last_name (required, 4-50 chars)
        - email (required, RFC-5322 validated, unique)
        - password (required, 5-8 chars, hashed via set_password)
        - photo (optional, JPG only, auto-resized to 300×300px)
    
    Success: Redirect to user-profile with session cookie set
    Error: Re-render form with validation errors
    """
    model = User
    template_name = 'authentication_user/registration_user.html'
    form_class = RegistrationUserForm
```

#### LoginUserView (authorization_user/views.py)
```python
class LoginUserView(AuthorizationUserMixin, LoginView):
    """
    User login endpoint.
    
    GET: Render login form
    POST: Authenticate email + password, create session
    
    Form fields:
        - username (actually email, via LoginUserForm override)
        - password
    
    Success: Create session, redirect to user-profile
    Error: Re-render form with error message
    """
    form_class = LoginUserForm
    template_name = 'authentication_user/login_user.html'
```

#### UserDetailView (authorization_user/views.py)
```python
class UserDetailView(AuthorizationUserMixin, DetailView):
    """
    User profile display (authenticated users only).
    
    URL: /authorization_user/user-profile/<pk>
    
    Displays:
        - First and last name
        - Email address
        - Profile photo (auto-resized to 300×300px)
        - Links to change password, logout
    
    Access Control: LoginRequiredMixin (via middleware or decorator)
    """
    model = User
    template_name = 'authentication_user/user_profile.html'
    context_object_name = 'users'
```

#### ChangeUserPasswordView (authorization_user/views.py)
```python
class ChangeUserPasswordView(AuthorizationUserMixin, PasswordChangeView):
    """
    Password change endpoint (authenticated users only).
    
    GET: Render password change form
    POST: Validate old password, hash new password, update
    
    Form fields:
        - old_password (current password verification)
        - new_password1 (new password)
        - new_password2 (confirmation)
    
    Success: Redirect to user-profile with success message
    Error: Re-render form with validation errors
    """
    template_name = 'authentication_user/change_password.html'
    form_class = ChangeUserPasswordForm
```

#### UserLogoutView (authorization_user/views.py)
```python
class UserLogoutView(LogoutView, AuthorizationUserMixin):
    """
    User logout endpoint.
    
    GET/POST: Flush session, delete session cookie, redirect to home
    
    Success: Redirect to main:home
    """
    http_method_names = ["post", "get"]
    template_name = 'authentication_user/logout_user.html'
```

### Mixin Pattern for Context Injection

```python
# authorization_user/utils.py
class AuthorizationUserMixin:
    """Injects common context variables (title) into template."""
    def get_mixin_context(self, context: dict, **kwargs):
        context.update(kwargs)
        return context

# Usage in views:
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return self.get_mixin_context(
        context=context,
        title='Login User'
    )
```

---

## Logging & Monitoring

### Current Logging Configuration

Django logs are configured in `settings.py`:

```python
# Default logging goes to console (development)
# In production, configure file handlers:

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/mysite.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Admin Activity Log

All admin actions are logged in the `django_admin_log` table:

```bash
# View admin actions via Django shell
python manage.py shell

>>> from django.contrib.admin.models import LogEntry
>>> entries = LogEntry.objects.all()
>>> for entry in entries:
...     print(f"{entry.user} - {entry.action_flag} - {entry.object_repr}")
```

### Access Application Logs

**Development** (console output):
```bash
python manage.py runserver
# Logs appear in terminal
```

**Production** (file-based):
```bash
tail -f /var/log/django/mysite.log
```

---

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test authorization_user

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Recommended Testing Libraries

```bash
pip install pytest pytest-django factory-boy
```

---

## Deployment Checklist

### Pre-Deployment Security Review

- [ ] `DEBUG = False` in production `settings.py`
- [ ] `SECRET_KEY` moved to environment variable
- [ ] `ALLOWED_HOSTS` restricted to your domain(s)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] Database migrated to PostgreSQL
- [ ] Static files collected via `collectstatic`
- [ ] Media files stored on cloud provider (S3, GCS)
- [ ] `.env` file in `.gitignore`
- [ ] Email backend configured (SendGrid, AWS SES)
- [ ] Logging configured to file or external service
- [ ] CORS headers configured if needed
- [ ] Rate limiting enabled on auth endpoints
- [ ] Security headers set (HSTS, CSP)

### Hosting Recommendations

- **Heroku**: Git-based deployment, easy PostgreSQL setup
- **DigitalOcean**: VPS with full control
- **AWS EC2**: Scalable cloud infrastructure
- **PythonAnywhere**: Beginner-friendly Python hosting

---

## Future Roadmap & Technical Debt

### High Priority (MVP Enhancement)

- [ ] **Email Verification**: Implement email confirmation on registration
- [ ] **Password Reset**: Forgot password flow with email token
- [ ] **Rate Limiting**: `django-ratelimit` on login endpoint
- [ ] **Two-Factor Authentication**: TOTP via `django-otp`
- [ ] **User Profile Edit**: Allow users to update name, email, photo
- [ ] **Admin Dashboard**: Statistics, user activity, system health

### Medium Priority (Scalability)

- [ ] **Caching**: Redis cache for session management
- [ ] **API Layer**: Django REST Framework for mobile/SPA clients
- [ ] **Background Tasks**: Celery + Redis for async operations
- [ ] **Search**: Elasticsearch for user directory
- [ ] **Monitoring**: Sentry for error tracking, DataDog for APM
- [ ] **Testing**: Pytest suite with >80% coverage

### Low Priority (Production Hardening)

- [ ] **Internationalization**: Multi-language support (i18n)
- [ ] **Accessibility**: WCAG 2.1 compliance (a11y)
- [ ] **Performance**: Database query optimization, CDN integration
- [ ] **Analytics**: User behavior tracking (privacy-compliant)
- [ ] **Compliance**: GDPR, CCPA data handling

### Known Limitations

1. **Single-Tenant**: No multi-tenancy support
2. **SQLite Production**: Not suitable for concurrent users
3. **Media Storage**: File storage not optimized for distributed systems
4. **Auth Only**: No role-based access control (RBAC) beyond Django groups
5. **Frontend**: Server-side rendering only; no SPA/API

---

## Contributing & Code Review

This repository is open to community feedback and pull requests.

**Code Style**: PEP 8 (via `black` and `flake8`)
**Testing**: All PRs must include tests
**Documentation**: Docstrings for all views, models, utilities

---

## License

This project is provided for educational and portfolio purposes. Specify your license here if sharing publicly.

---

## Support & Questions

For questions, issues, or feedback:
- 📧 Email: mihaiapostol14@example.com
- 💼 LinkedIn: [Profile Link]
- 🐙 GitHub Issues: [GitHub Issues Link]

---

## Changelog

### v1.0.0 (Initial Release)
- ✓ User registration with email-based authentication
- ✓ Login/logout functionality
- ✓ User profile with photo upload
- ✓ Password change capability
- ✓ SQLite development database
- ✓ Responsive Bootstrap UI
- ✓ Admin panel integration

---

**Last Updated**: July 1, 2026  
**Django Version**: 5.2.8  
**Python Version**: 3.10+  
**Repository**: https://github.com/mihaiapostol14/My_Django_Site
