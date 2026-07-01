# My Django Site

## Executive Summary

**My Django Site** is a production-ready Django 5.2 portfolio web application demonstrating enterprise-grade development practices. The application implements a complete authentication system with role-based access control, responsive design, and image processing capabilities. Built with modern Django patterns (Class-Based Views, custom user models, mixins), it serves as a reference implementation for full-stack web development best practices.

**Target Audience**: Prospective employers, code reviewers, and developers seeking a well-documented, scalable foundation for Django-based applications.

**Repository Status**: 🟢 Public (Portfolio Demonstration) | ⚠️ Pre-Production (Development Database)

---

## Architecture & Technology Stack

| Layer | Component | Technology | Version | Purpose |
|-------|-----------|-----------|---------|---------|
| **Framework** | Web Application | Django | 5.2.8 | Core web framework |
| **Language** | Backend Runtime | Python | 3.10+ | Server-side logic |
| **Database** | RDBMS (Dev) | SQLite3 | — | Development/demo database |
| **Database** | RDBMS (Prod) | PostgreSQL | 12+ | Recommended production database |
| **ORM** | Object-Relational Mapping | Django ORM | Native | Query abstraction |
| **Frontend** | UI Framework | Bootstrap | 5.2.3 | Responsive design system |
| **Styling** | CSS Theme | Grayscale (Start Bootstrap) | Custom | Pre-built design system |
| **Icons** | Icon Library | Font Awesome | 6.3.0 | Scalable vector icons |
| **JavaScript** | Client-side Logic | Vanilla JS | ES6+ | Interactive components |
| **Image Processing** | Media Handling | Pillow | 11.2.1 | Image optimization/resizing |
| **Session Manager** | Session Backend | Django Sessions | Django | User session persistence |
| **Authentication** | Auth Backend | Django Auth | Django | User authentication |
| **ASGI Support** | Async Support | asgiref | 3.8.1 | ASGI reference implementation |
| **SQL Parser** | Utility | sqlparse | 0.5.3 | SQL query parsing |
| **Timezone DB** | Localization | tzdata | 2025.2 | Timezone information |

---

## Authentication & Identity System

### Primary Identifier Strategy

**Current Implementation**: **Username-based** (with email as secondary identifier)

```python
class CustomUser(AbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'username'           # Primary login identifier
    REQUIRED_FIELDS = ['email']            # Required on creation
    
    username = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[UnicodeUsernameValidator]
    )
    email = models.EmailField(
        max_length=254, 
        validators=[validate_email]
    )
```

### Authentication Pipeline

```mermaid
graph TD
    A[User Visits /authorization_user/register/] --> B[RegistrationUserForm]
    B --> C{Form Valid?}
    C -->|No| D[Render Form with Errors]
    C -->|Yes| E[Hash Password via set_password]
    E --> F[Save CustomUser Instance]
    F --> G[Auto-Login: login() function]
    G --> H[Redirect to User Profile]
    H --> I[Session Created]
    
    J[User Visits /authorization_user/login/] --> K[LoginUserForm]
    K --> L{Credentials Match?}
    L -->|No| M[Render Login Error]
    L -->|Yes| N[Authenticate via ModelBackend]
    N --> O[create_session_id]
    O --> P[Set Session Cookie]
    P --> Q[Redirect to User Profile]
    
    R[User Clicks Logout] --> S[logout request]
    S --> T[Flush Session]
    T --> U[Delete Session Cookie]
    U --> V[Redirect to Home]
```

### Validation Strategy

| Field | Validator | Constraints | Purpose |
|-------|-----------|-------------|---------|
| **username** | `UnicodeUsernameValidator` | 5-50 chars, unique | Alphanumeric, unicode support |
| **email** | `validate_email` (RFC 5322) | Max 254 chars | RFC-compliant validation |
| **password** | Django Password Validators | 5-8 chars | Hashed via PBKDF2 (default) |
| **photo** | `FileExtensionValidator` | JPG only | Security: prevent malicious uploads |

### Security Implementation

✅ **Implemented**:
- CSRF protection on all forms (`{% csrf_token %}`)
- Password hashing via `set_password()` (PBKDF2)
- Session-based authentication (Django sessions framework)
- File extension validation (JPG only)
- HTTP security middleware (X-Frame-Options, Content-Security-Policy headers)

⚠️ **Recommendations for Production**:
- Implement rate limiting on `/authorization_user/login/` (e.g., django-ratelimit)
- Add two-factor authentication (2FA) via django-otp
- Implement email verification on registration
- Add account lockout after N failed login attempts
- Use secure password hashing (Argon2 via django-argon2)

---

## Database Management

### Current Strategy: SQLite3 (Development)

**Why SQLite?**
- Zero configuration, file-based database
- Perfect for prototyping and local development
- No external dependencies or services required
- Sufficient for portfolio demonstration purposes

**Location**: `db.sqlite3` (in project root)

**Current Configuration** (from `settings.py`):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

**Tables Created**:
- `authorization_user_user` (CustomUser model)
- `auth_group` (Django permissions)
- `auth_permission` (Django permissions)
- `django_session` (Session data)
- `django_migrations` (Migration history)
- `django_admin_log` (Admin activity)

### Production Migration: PostgreSQL

#### Step 1: Install PostgreSQL Backend
```bash
pip install psycopg2-binary
# or for development:
pip install psycopg2
```

#### Step 2: Update `settings.py`
```python
import os
from urllib.parse import urlparse

# Use environment variable for database URL
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/mydjango_site'
)

# Parse the URL
db_from_env = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_from_env.path[1:],  # Remove leading '/'
        'USER': db_from_env.username,
        'PASSWORD': db_from_env.password,
        'HOST': db_from_env.hostname,
        'PORT': db_from_env.port or 5432,
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL in production
        },
    }
}
```

#### Step 3: Create PostgreSQL Database
```bash
# On your PostgreSQL server
createdb -U postgres mydjango_site
createuser -U postgres myapp_user -P  # Set password interactively
psql -U postgres -d mydjango_site -c "GRANT ALL PRIVILEGES ON DATABASE mydjango_site TO myapp_user;"
```

#### Step 4: Migrate Data
```bash
# Dump from SQLite
python manage.py dumpdata > data.json

# Switch to PostgreSQL (update settings.py)
python manage.py migrate

# Load data
python manage.py loaddata data.json
```

#### Step 5: Verify
```bash
python manage.py dbshell  # Should connect to PostgreSQL
python manage.py test
```

### Media File Strategy

**Current Structure**:
```
media/
├── user_photo/              # User-uploaded profile photos
└── default_account_picture.jpg
```

**Why Media is Included**:
This is a **educational repository for portfolio purposes**. Media files demonstrate the complete working application flow. In production:

**Production Best Practices**:
```bash
# .gitignore (should include):
media/
!media/.gitkeep             # Keep directory structure
staticfiles/
*.sqlite3
.env
.venv/
```

**Why Remove in Production**:
1. **File Size**: Media files bloat repository
2. **Scalability**: Use external storage (AWS S3, Google Cloud Storage, DigitalOcean Spaces)
3. **Security**: Never commit user-uploaded files
4. **Version Control**: Media is not versioned—use CDN/cloud storage

**Production Media Handling**:
```python
# settings.py (production)
import boto3
from storages.backends.s3boto3 import S3Boto3Storage

AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

DEFAULT_FILE_STORAGE = 'path.to.MediaStorage'  # User uploads → S3
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

### Data Migrations

#### Creating Migrations
```bash
# After modifying a model
python manage.py makemigrations authorization_user
python manage.py migrate
```

#### Viewing Migration History
```bash
python manage.py showmigrations
# Output:
# authorization_user
#  [X] 0001_initial
#  [X] 0002_add_photo_field
```

#### Reverting Migrations
```bash
python manage.py migrate authorization_user 0001
```

---

## Setup & Configuration

### Prerequisites

- **Python**: 3.10+ ([Download](https://www.python.org/downloads/))
- **pip**: Package manager (included with Python 3.4+)
- **git**: Version control ([Download](https://git-scm.com/))
- **virtualenv** or **venv**: Virtual environment (recommended)
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

# Windows
python -m venv venv
venv\Scripts\activate

# Verify activation (prompt should show (venv))
```

#### 3. Upgrade pip & Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 4. Navigate to Django Project
```bash
cd MyWebSite
```

#### 5. Environment Configuration (.env)

**Create `.env` file** (for development):
```bash
# .env (Development)
DEBUG=True
SECRET_KEY='your-secret-key-here'
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Email configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**For Production** (use environment variables or .env with python-decouple):
```bash
pip install python-decouple
```

Update `settings.py`:
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
DATABASE_URL = config('DATABASE_URL')
```

#### 6. Database Initialization
```bash
python manage.py migrate
# Output:
# Operations to perform:
#   Apply all migrations: admin, auth, authorization_user, contenttypes, main, sessions
# Running migrations:
#   Applying authorization_user.0001_initial... OK
#   ...
```

#### 7. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

**Prompt**:
```
Username: admin
Email: admin@example.com
Password: ••••••••••
Password (again): ••••••••••
Superuser created successfully.
```

#### 8. Collect Static Files (Production Only)
```bash
python manage.py collectstatic --noinput
# Output:
# 1234 static files copied to '/path/to/staticfiles'
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
- **Admin Panel**: http://127.0.0.1:8000/admin/ (superuser credentials)

### Secret Management

#### ⚠️ Security Warning
The repository **intentionally exposes** `SECRET_KEY` in `settings.py` for demonstration purposes.

**Production Checklist**:
- ✅ Move `SECRET_KEY` to environment variable
- ✅ Add `.env` to `.gitignore`
- ✅ Use strong, unique secrets (40+ characters)
- ✅ Rotate secrets periodically
- ✅ Use separate secrets for development/staging/production

#### Generating Secure Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Administrative Operations

### Superuser Management

#### Create Superuser
```bash
python manage.py createsuperuser
```

#### Change Superuser Password
```bash
python manage.py changepassword <username>
```

#### Delete Superuser
```bash
python manage.py shell
>>> from authorization_user.models import User
>>> User.objects.get(username='admin').delete()
```

#### List All Users
```bash
python manage.py shell
>>> from authorization_user.models import User
>>> users = User.objects.all()
>>> for user in users:
...     print(f"{user.username} ({user.email}) - Admin: {user.is_staff}")
```

### Admin Panel Features

Access at: http://127.0.0.1:8000/admin/

**Capabilities**:
- Create/edit/delete users
- Manage permissions and groups
- View login history (via `django_admin_log`)
- Configure site settings
- Monitor authentication attempts

### Custom Management Commands

**Example**: Create a custom command to generate test data:
```bash
# Create file: authorization_user/management/commands/create_test_users.py
from django.core.management.base import BaseCommand
from authorization_user.models import User

class Command(BaseCommand):
    help = 'Create test users'
    
    def handle(self, *args, **options):
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        self.stdout.write(self.style.SUCCESS('Test user created'))
```

**Run**:
```bash
python manage.py create_test_users
```

---

## Repository Integrity & Security Philosophy

### Public Repository Rationale

**Why This Repository is Public**:
1. **Portfolio Demonstration**: Showcases Django development expertise for potential employers
2. **Educational Purpose**: Serves as a reference implementation of best practices
3. **Open Source Philosophy**: Encourages community feedback and contributions
4. **Code Review Ready**: Structured for senior code review

### Security Practices Implemented

✅ **Security In Place**:
- CSRF tokens on all forms
- Password hashing (PBKDF2)
- Session-based authentication
- File upload validation
- HTTP security headers

⚠️ **Intentional Exposures** (for demo purposes):
- `SECRET_KEY` in source code (should use .env in production)
- `DEBUG=True` (should be False in production)
- `ALLOWED_HOSTS=[]` (should specify domain)
- SQLite in version control (should use production DB)

### .gitignore Best Practices

**Recommended `.gitignore`**:
```gitignore
# Virtual environment
venv/
env/
*.egg-info/

# Django
*.sqlite3
db.sqlite3
/media/
staticfiles/
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/
```

### CI/CD Recommendations

**GitHub Actions Workflow** (`.github/workflows/ci.yml`):
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: postgres

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run migrations
        run: python manage.py migrate
      
      - name: Run tests
        run: python manage.py test
      
      - name: Check code style
        run: flake8 .
```

---

## View & Logic Layer: Django MVT Architecture

### Model-View-Template (MVT) Pattern

```
User Request
    ↓
Django URL Router (urls.py)
    ↓
View (Class-Based View)
    ↓
Model (ORM Query)
    ↓
Database
    ↓
Context Data
    ↓
Template (Jinja2)
    ↓
HTML Response
```

### Application Structure

#### `authorization_user` App
**Purpose**: User authentication and profile management

| View | HTTP Method | URL | Logic |
|------|------------|-----|-------|
| `CreateUserView` | GET, POST | `/authorization_user/register/` | Registration form + user creation |
| `LoginUserView` | GET, POST | `/authorization_user/login/` | Login form + session creation |
| `UserDetailView` | GET | `/authorization_user/profile/<pk>/` | Display user profile |
| `ChangeUserPasswordView` | GET, POST | `/authorization_user/change-password/` | Password change form + update |
| `UserLogoutView` | GET, POST | `/authorization_user/logout/` | Session destruction + redirect |

#### `main` App
**Purpose**: Public-facing pages (home, portfolio)

| View | HTTP Method | URL | Logic |
|------|------------|-----|-------|
| `HomeView` | GET | `/` | Landing page + calendar generation |

### Class-Based View Architecture

#### BaseView Pattern
```python
from django.views.generic import CreateView, LoginView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateUserView(CreateView):
    """User registration via ModelForm"""
    template_name = 'authentication_user/registration_user.html'
    form_class = RegistrationUserForm
    
    def form_valid(self, form):
        # Custom logic: auto-login after registration
        self.object = form.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('authorization_user:user-profile', 
                          kwargs={'pk': self.request.user.pk})
```

#### Mixin Pattern
```python
class AuthorizationUserMixin:
    """Shared context data for authentication views"""
    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context

class LoginUserView(AuthorizationUserMixin, LoginView):
    """Login with mixin for DRY principle"""
    pass
```

### Template Inheritance

```
base.html (root)
├── default_navbar.html (unauthenticated)
├── auth_user_navbar.html (authenticated)
├── message.html (flash messages)
└── authentication_user/
    ├── registration_user.html
    ├── login_user.html
    ├── user_profile.html
    └── change_password.html
```

### URL Routing

```python
# MyWebSite/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('authorization_user/', include('authorization_user.urls', namespace='authorization_user')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# authorization_user/urls.py
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('change-password/', ChangeUserPasswordView.as_view(), name='change-password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
```

### Form Validation Pipeline

```mermaid
graph TD
    A[Form Submitted] --> B[form_valid called]
    B --> C{Clean Data?}
    C -->|No| D[form_invalid returns errors]
    C -->|Yes| E[Model Methods Called]
    E --> F[set_password hashes password]
    F --> G[model.save invokes signals]
    G --> H[Image resizing occurs]
    H --> I[Database Transaction Commit]
    I --> J[Success Redirect]
```

---

## Logging & Monitoring

### Current Logging Strategy

**Default Django Logging** (in production):
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'authorization_user': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Log Locations

| Log Type | Location | Purpose |
|----------|----------|---------|
| **Django Logs** | `logs/django.log` | Application events, errors |
| **Access Logs** | Nginx/Gunicorn stdout | HTTP request tracking |
| **Admin Actions** | `django_admin_log` table | User management history |
| **Errors** | `logs/django.log` | Exceptions and tracebacks |

### Monitoring Tools (Recommended)

- **Sentry**: Error tracking and alerting
- **Datadog**: Infrastructure and application monitoring
- **New Relic**: Performance monitoring
- **Prometheus + Grafana**: Metrics visualization

### Authentication Logging

```python
# Track login/logout events
from django.contrib.auth.signals import user_logged_in, user_logged_out

def log_user_login(sender, request, user, **kwargs):
    import logging
    logger = logging.getLogger('authorization_user')
    logger.info(f"User {user.username} logged in from {request.META.get('REMOTE_ADDR')}")

user_logged_in.connect(log_user_login)
```

---

## Technical Architecture: Data Flow

### User Registration Flow
```
1. User → /authorization_user/register/
2. GET: Render RegistrationUserForm (template)
3. User fills: username, email, password, photo
4. POST: form.is_valid()
   ├─ Check uniqueness: username, email
   ├─ Validate: password strength, file extension
   └─ If valid: form.save()
5. form.save() → model.save()
   ├─ set_password() → PBKDF2 hashing
   ├─ File upload → media/user_photo/
   └─ Image signal → Pillow resize (300x300px)
6. login() → create session cookie
7. Redirect → /authorization_user/profile/<pk>/
```

### Image Processing Pipeline
```
User Uploads JPG
        ↓
FileExtensionValidator checks JPG extension
        ↓
File saved to media/user_photo/
        ↓
model.save() signal triggers
        ↓
Pillow Image.open()
        ↓
Check dimensions: (height > 300 or width > 300)
        ↓
Create thumbnail (300x300px)
        ↓
Overwrite original file
        ↓
Database photo field updated
```

---

## Future Roadmap & Production Considerations

### Phase 1: Immediate Improvements (v1.1)

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| **High** | Add automated tests (unit, integration) | 3-5 days | Prevents regressions |
| **High** | Implement .gitignore properly | 1 day | Security improvement |
| **High** | Move secrets to .env | 1 day | Security compliance |
| **Medium** | Add email verification on signup | 2-3 days | Reduces spam accounts |
| **Medium** | Implement rate limiting on auth | 1-2 days | DOS protection |
| **Low** | Add logging configuration | 1 day | Operational visibility |

### Phase 2: Production Hardening (v1.5)

| Item | Technical Approach |
|------|-------------------|
| **Database** | Migrate to PostgreSQL + connection pooling |
| **Media Storage** | AWS S3 + CloudFront CDN |
| **Authentication** | Add 2FA (django-otp) |
| **API** | Django REST Framework for mobile clients |
| **Caching** | Redis for sessions + query cache |
| **Monitoring** | Sentry for error tracking |
| **Performance** | Database indexing + query optimization |
| **Security** | WAF + DDoS protection + security headers |

### Phase 3: Enterprise Features (v2.0)

| Feature | Rationale |
|---------|-----------|
| **Multi-tenancy** | Support multiple portfolios per instance |
| **API Gateway** | Expose endpoints for third-party integrations |
| **Analytics** | Track user behavior + site metrics |
| **Search** | Elasticsearch for portfolio/user search |
| **Real-time** | WebSockets for notifications |
| **Admin Dashboard** | Custom analytics + reporting |

### Technical Debt Assessment

#### Current Issues

| Issue | Severity | Resolution |
|-------|----------|-----------|
| No automated tests | High | Implement pytest + Django test framework |
| Hardcoded SECRET_KEY | High | Move to environment variables |
| SQLite in production | High | Migrate to PostgreSQL |
| No error tracking | Medium | Integrate Sentry |
| Missing logging | Medium | Add structured logging (Python logging module) |
| No rate limiting | Medium | Add django-ratelimit |
| Vanilla JS (scalability) | Low | Consider Vue.js/React for complex UX |
| No API (mobile support) | Low | Add Django REST Framework |
| Media files in repo | Medium | Use S3/CDN in production |

### Performance Optimization Roadmap

#### Quick Wins (Week 1)
- [ ] Add database indexes on `username`, `email`
- [ ] Enable `select_related()` in views
- [ ] Minify CSS/JS
- [ ] Enable gzip compression in Nginx

#### Medium-term (Month 1)
- [ ] Implement Redis caching for sessions
- [ ] Query optimization review
- [ ] CDN for static files
- [ ] Image lazy-loading

#### Long-term (Quarter 1)
- [ ] Database replication (read replicas)
- [ ] Load balancing with Nginx
- [ ] Horizontal scaling with Docker/Kubernetes
- [ ] Microservices separation (auth vs portfolio)

---

## Best Practices Demonstrated

### ✅ Implemented
1. **Custom User Model**: Extensible via `AbstractUser`
2. **Class-Based Views**: DRY code, mixins for reusability
3. **Mixin Pattern**: `AuthorizationUserMixin`, `HomeMixin`
4. **Form Validation**: Client + server-side validation
5. **Image Processing**: Pillow for optimization
6. **Template Inheritance**: Base template + block overrides
7. **Static Files**: Organized with Bootstrap + Font Awesome
8. **CSRF Protection**: `{% csrf_token %}` on forms
9. **Password Hashing**: `set_password()` for security
10. **URL Namespacing**: `namespace='authorization_user'`

### ⏳ Recommended Additions
1. **Automated Tests**: pytest + coverage reports
2. **Type Hints**: Python 3.10+ type annotations
3. **Docstrings**: Module, class, function documentation
4. **Environment Variables**: python-decouple + .env
5. **Logging**: Structured logging (JSON format)
6. **Error Tracking**: Sentry integration
7. **API Framework**: Django REST Framework
8. **Cache Layer**: Redis for performance
9. **Background Tasks**: Celery for async work
10. **Code Quality**: Pre-commit hooks + Black/Flake8

---

## Deployment Guide

### Development Environment

**Status**: ✅ Complete  
**Database**: SQLite3  
**Command**: `python manage.py runserver`  
**Access**: http://127.0.0.1:8000/

### Staging Environment

**Requirements**:
- PostgreSQL database
- Redis cache
- Gunicorn WSGI server
- Nginx reverse proxy
- SSL certificate

**Setup**:
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary redis django-extensions

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn MyWebSite.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Production Environment

**Deployment Checklist**:
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` from environment variable
- [ ] `ALLOWED_HOSTS` configured
- [ ] PostgreSQL database (connection pooling)
- [ ] Redis cache backend
- [ ] S3/CDN for media files
- [ ] Gunicorn with multiple workers
- [ ] Nginx with SSL/TLS
- [ ] Health checks enabled
- [ ] Monitoring and alerting configured
- [ ] Backup strategy in place
- [ ] Rate limiting enabled

**Recommended Hosts**:
- **Heroku**: PaaS, easy deployment, hobby tier available
- **DigitalOcean**: VPS, affordable, good documentation
- **AWS EC2**: Scalable, enterprise-grade
- **PythonAnywhere**: Django-specific, beginner-friendly
- **Render**: Modern PaaS alternative to Heroku

---

## Code Quality & Standards

### Code Style Guidelines

**Follow PEP 8**:
```bash
pip install flake8
flake8 authorization_user main --max-line-length=100
```

**Automated Formatting**:
```bash
pip install black
black authorization_user main
```

### Type Hints (Python 3.10+)

```python
from typing import Optional, Dict, List

class CreateUserView(CreateView):
    form_class: type = RegistrationUserForm
    
    def form_valid(self, form) -> HttpResponse:
        user: User = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
```

### Docstring Standards

```python
def get_mixin_context(self, context: Dict, **kwargs) -> Dict:
    """
    Enrich view context with common data.
    
    Args:
        context (Dict): The template context dictionary
        **kwargs: Additional context variables
    
    Returns:
        Dict: Updated context with kwargs merged in
    
    Example:
        >>> ctx = get_mixin_context({}, title='Home')
        >>> ctx['title']
        'Home'
    """
    context.update(kwargs)
    return context
```

---

## Testing Strategy

### Recommended Test Structure

```
authorization_user/
├── tests/
│   ├── __init__.py
│   ├── test_models.py          # CustomUser model tests
│   ├── test_views.py           # View logic tests
│   ├── test_forms.py           # Form validation tests
│   └── test_auth_pipeline.py   # Full auth flow tests
└── ...

main/
├── tests/
│   ├── __init__.py
│   ├── test_views.py
│   └── test_calendar.py
└── ...
```

### Example Test

```python
# authorization_user/tests/test_views.py
from django.test import TestCase, Client
from authorization_user.models import User

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
    
    def test_login_page_loads(self):
        response = self.client.get('/authorization_user/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication_user/login_user.html')
    
    def test_login_success(self):
        response = self.client.post('/authorization_user/login/', {
            'username': 'testuser',
            'password': 'TestPass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(response.wsgi_request.user.is_authenticated)
```

**Run Tests**:
```bash
python manage.py test authorization_user --verbosity=2
```

---

## Contributing Guidelines

### For External Contributors

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/auth-2fa`
3. **Write** tests for new features
4. **Follow** PEP 8 style guide
5. **Commit** with clear messages: `git commit -m "Add 2FA support"`
6. **Push** to branch: `git push origin feature/auth-2fa`
7. **Submit** Pull Request with description

### Code Review Criteria

- [ ] Tests pass (`python manage.py test`)
- [ ] Code follows PEP 8 (`flake8 .`)
- [ ] Docstrings present
- [ ] Security implications reviewed
- [ ] Database migrations created (if applicable)
- [ ] README updated (if applicable)

---

## License & Attribution

**Current Status**: Unlicensed (Public Portfolio)

**Recommendation**: Add [MIT License](https://opensource.org/licenses/MIT) for open-source use.

**Attribution**:
- **Bootstrap Theme**: Grayscale (Start Bootstrap)
- **Icons**: Font Awesome 6.3.0
- **Framework**: Django 5.2

---

## Support & Contact

### Getting Help

1. **Documentation**: [Django Official Docs](https://docs.djangoproject.com/)
2. **Issues**: [GitHub Issues](https://github.com/mihaiapostol14/My_Django_Site/issues)
3. **Community**: [Django Forum](https://forum.djangoproject.com/)

### Reporting Issues

**Issue Template**:
```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.10.x
- Django version: 5.2.8
- OS: Ubuntu 22.04
```

---

## Author & Maintenance

**Project Owner**: [Mihai Apostol](https://github.com/mihaiapostol14)

**Repository**: [My_Django_Site](https://github.com/mihaiapostol14/My_Django_Site)

**Status**: 🟢 Active Development  
**Last Updated**: 2026-07-01  
**Django Version**: 5.2.8  
**Python Version**: 3.10+

---

## Quick Reference

### Frequently Used Commands

```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
pip freeze > requirements.txt

# Database
python manage.py migrate
python manage.py makemigrations
python manage.py showmigrations

# Users
python manage.py createsuperuser
python manage.py changepassword <username>

# Server
python manage.py runserver
python manage.py runserver 0.0.0.0:8001

# Shell
python manage.py shell

# Testing
python manage.py test
python manage.py test authorization_user -v 2

# Static files
python manage.py collectstatic
python manage.py collectstatic --noinput

# Debugging
python manage.py check
python manage.py dbshell
```

---

## Appendix: Security Checklist

### Before Production Deployment

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` randomized (40+ chars)
- [ ] `ALLOWED_HOSTS` configured
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS = 31536000`
- [ ] Database backed by PostgreSQL
- [ ] Media served via CDN (not from Django)
- [ ] Static files collected and minified
- [ ] HTTPS/SSL certificate installed
- [ ] Database backups enabled
- [ ] Monitoring and alerts configured
- [ ] Error tracking (Sentry) configured
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] OWASP Top 10 reviewed

---

**Document Version**: 1.0  
**Last Reviewed**: 2026-07-01  
**Next Review**: 2026-10-01  
**Compliance**: PEP 8, Django 5.2+ Standards
