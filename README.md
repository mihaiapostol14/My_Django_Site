# My Django Site

## Project Overview

My Django Site is a full-stack web application built with Django 5.2, providing a modern, responsive portfolio platform with integrated user authentication and role-based content delivery. The application leverages Bootstrap 5 for responsive design, implements dual navigation architecture based on authentication state, and delivers a professional user experience with form validation and session management. The system maintains a SQLite database with user profiles, supports image uploads, and provides secure credential management for registered users.

## Tech Stack

- **Backend**: Python, Django 5.2, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Framework**: Bootstrap 5.2.3, Font Awesome 6.3.0
- **Database**: SQLite3
- **Dependencies**: Pillow (image processing), asgiref, sqlparse, tzdata


## Installation & Setup

### Prerequisites

Ensure your system has the following installed:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager - typically included with Python)
- **git** (for version control)
- **virtualenv** or **venv** (Python virtual environment)

### Step 1: Clone the Repository

```bash
git clone https://github.com/mihaiapostol14/My_Django_Site.git
cd My_Django_Site
```

### Step 2: Create Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Installed Packages:**
```
asgiref==3.8.1          # ASGI reference implementation
Django==5.2.8            # Web framework
pillow==11.2.1           # Image processing library
sqlparse==0.5.3          # SQL parser utility
tzdata==2025.2           # Timezone database
```

### Step 4: Navigate to Project Directory

```bash
cd MyWebSite
```

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database and initializes all Django tables:
- `django_migrations`
- `django_users` (custom)
- `auth_*` (permission tables)

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 8: Access the Application

- **Frontend:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/ (use superuser credentials)

---

## Detailed Features

### Authentication & User Management

- **User Registration**: Multi-field registration system with username, email, password, and profile photo upload capability. Form validation ensures data integrity and provides real-time feedback.
- **Secure Login**: Authentication mechanism with CSRF protection, session management, and credential validation. Includes "forgot password" recovery flow.
- **Password Management**: Change password functionality with secure password update mechanism. Users can reset credentials post-registration.
- **User Profiles**: Personalized user profile pages displaying authenticated user information. Dynamic navbar rendering based on authentication state.

### Navigation & Routing

- **Dynamic Navbar**: Context-aware navigation menu that conditionally renders based on user authentication status:
  - **Unauthenticated Users**: Registration and login links
  - **Authenticated Users**: Profile access, logout functionality, and projects section
- **Fixed Navigation**: Bootstrap sticky navbar with smooth scrolling and responsive collapse functionality for mobile devices.

### UI/UX Components

- **Responsive Design**: Mobile-first CSS architecture using Bootstrap 5 grid system with adaptive viewport configurations for all device sizes.
- **Interactive Scrolling**: JavaScript-driven navbar shrink effect triggered on page scroll events. ScrollSpy integration for active navigation link highlighting during multi-section navigation.
- **Form Validation**: Client-side HTML5 validation with custom Bootstrap feedback messaging. Graceful error state handling and visual feedback.
- **Icon Integration**: Font Awesome icon library (6.3.0) for consistent, scalable iconography across contact and social media sections.

### Page Structure

- **Masthead Section**: Hero landing section with personalized user greeting, call-to-action button, and typography-driven visual hierarchy.
- **About Section**: Content showcase featuring Bootstrap theme information with responsive image embedding.
- **Projects Section**: Multi-column project portfolio with alternating image/text layouts. Featured project row with expanded description space.
- **Signup Section**: Email subscription form with SB Forms integration (extensible for email marketing services).
- **Contact Section**: Three-column contact card layout displaying address, email, and phone information. Social media integration links (Twitter, Facebook, GitHub).
- **Footer**: Copyright information and site attribution with minimal design footprint.

### Frontend Interactions

- **Navbar Event Handling**: DOMContentLoaded event listener initializing navbar shrink functionality on page load and scroll events. Bootstrap ScrollSpy activation for navigation state tracking.
- **Responsive Toggler**: Mobile hamburger menu toggle with automatic collapse on nav link click to improve UX on smaller screens.
- **Form State Management**: Dynamic form validation feedback with Bootstrap validation classes applied on user input.

### Static Assets

- **CSS Architecture**: Comprehensive 246KB stylesheet (`styles.css`) implementing Grayscale theme from Start Bootstrap. Includes responsive breakpoints, accessibility-compliant color schemes, and animation effects.
- **JavaScript Utilities**: Modular script architecture with event delegation and DOM manipulation for progressive enhancement.
- **Media Resources**: Directory structure supporting user-uploaded media files (photos) and theme assets (icons, images).

## Class-Based Views Architecture

The application implements Django's Class-Based Views (CBV) pattern for maintainable, reusable, and extensible request handling. All views leverage mixins for shared functionality and proper separation of concerns.

### Authentication Views

#### **CreateUserView**

Handles user registration with model form validation and automatic login after successful registration.

```python
class CreateUserView(CreateView, AuthorizationUserMixin):
    template_name = 'authentication_user/registration_user.html'
    form_class = RegistrationUserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, user=self.object, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Django already handles rendering the form with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Registration User')

    def get_success_url(self):
        messages.success(request=self.request, message=f'Registration {self.request.user} Successful')
        return reverse_lazy('authorization_user:user-profile', kwargs={'pk': self.request.user.pk})
```

**Features**:
- Inherits from `CreateView` for model creation and `AuthorizationUserMixin` for context
- Overrides `form_valid()` to automatically authenticate user after registration
- Custom success message via Django messages framework
- Redirects to user profile on successful registration

---

#### **LoginUserView**

Handles user login with credentials validation and session management.

```python
class LoginUserView(AuthorizationUserMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication_user/login_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Login User')

    def get_success_url(self):
        messages.success(request=self.request, message=f'Login {self.request.user} Successful')
        return reverse_lazy('authorization_user:user-profile', kwargs={'pk': self.request.user.pk})
```

**Features**:
- Inherits from `LoginView` (Django's built-in authentication view)
- CSRF protection and session management handled automatically
- Custom form validation through `LoginUserForm`
- Redirects authenticated users to profile page
- Success message notification on login

---

#### **UserDetailView**

Displays authenticated user profile information.

```python
class UserDetailView(AuthorizationUserMixin, DetailView):
    model = User
    template_name = 'authentication_user/user_profile.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)
```

**Features**:
- Inherits from `DetailView` for single object display
- Model lookup from `CustomUser` by primary key
- Custom context object name for template rendering
- Authorization enforcement via mixin

---

#### **ChangeUserPasswordView**

Handles secure password change requests with validation.

```python
class ChangeUserPasswordView(AuthorizationUserMixin, PasswordChangeView):
    template_name = 'authentication_user/change_password.html'
    form_class = ChangeUserPasswordForm

    def get_success_url(self):
        messages.success(request=self.request, message=f'Change Password {self.request.user} Successful')
        return reverse_lazy('authorization_user:user-profile', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)
```

**Features**:
- Inherits from `PasswordChangeView` (Django's built-in password change)
- Validates old password before allowing update
- Updates authentication backend with new credentials
- Redirects to profile on success with notification

---

#### **UserLogoutView**

Clears session and authentication cookies.

```python
class UserLogoutView(LogoutView, AuthorizationUserMixin):
    http_method_names = ["post", "get"]
    template_name = 'authentication_user/logout_user.html'

    def get_success_url(self):
        return reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Logout {self.request.user}')
```

**Features**:
- Inherits from `LogoutView` for session termination
- Supports both GET and POST HTTP methods
- Clears session and authentication cookies automatically
- Redirects to home page after logout

---

### Main Application Views

#### **HomeView**

Renders landing page with portfolio showcase and calendar generation.

```python
class HomeView(HomeMixin, TemplateView):
    template_name = 'main/home.html'

    @staticmethod
    def put_calendar(year: int = datetime.now().year, month: str = datetime.now().strftime('%B')):
        month = month.capitalize()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)
        return HTMLCalendar().formatmonth(year, month_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Home', calendar_object=self.put_calendar)
```

**Features**:
- Inherits from `TemplateView` for static content rendering
- `put_calendar()` static method:
  - Accepts optional `year` and `month` parameters (defaults to current)
  - Converts month name to integer
  - Returns formatted HTML calendar using `HTMLCalendar().formatmonth()`
- Passes calendar callable to template context for dynamic rendering
- Manages authenticated/unauthenticated display logic

---

### Mixin Architecture

#### **AuthorizationUserMixin**

Provides shared context data across authentication views.

```python
class AuthorizationUserMixin:
    def get_mixin_context(self, context, **kwargs):
        # Enriches context with common data for auth views
        context.update(kwargs)
        return context
```

**Purpose**:
- Centralized context data management
- DRY principle across all auth-related views
- Consistent title setting and template variables

---

#### **HomeMixin**

Provides shared context data for home view.

```python
class HomeMixin:
    def get_mixin_context(self, context, **kwargs):
        # Enriches context with home-specific data
        context.update(kwargs)
        return context
```

**Purpose**:
- Home-specific logic centralization
- Calendar generation context injection
- Template variable consistency

---

### Form Classes

#### **RegistrationUserForm**

Multi-field registration form with validation.

```python
class RegistrationUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ''

        self.fields['username'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'username',
            'id': 'username',
            'class': 'form-control',
            'placeholder': 'Peter',
            'value': '',
            'maxlength': '50',
            'minlength': '5'
        }),

        self.fields['email'].widget.attrs.update({
            'required': '',
            'type': 'email',
            'name': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'PiterParker@gmail.com',
            'value': ''
        })

        self.fields['password'].widget.attrs.update({
            'required': '',
            'type': 'password',
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'PiterParker1234',
            'value': '',
            'maxlength': '8',
            'minlength': '5'
        })

        self.fields['photo'].widget.attrs.update({
            'type': 'file',
            'name': 'photo',
            'id': 'photo',
            'class': 'form-control',
            'maxlength': '8',
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'photo']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password': "Password",
            'photo': 'Upload Your Photo',
        }

        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

**Fields & Validation**:
- **username**: 5-50 characters, unicode support, unique constraint
- **email**: RFC-compliant validation, required
- **password**: 5-8 characters, hashed on save via `set_password()`
- **photo**: JPG extension only, required

---

#### **LoginUserForm**

Login credentials form with Bootstrap styling.

```python
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username', 'password']
```

**Features**:
- Inherits from `AuthenticationForm` for built-in validation
- Bootstrap form control styling
- Supports custom user model authentication

---

#### **ChangeUserPasswordForm**

Password change form with confirmation matching.

```python
class ChangeUserPasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
```

**Features**:
- Inherits from `PasswordChangeForm` for password validation
- Confirms password match
- Bootstrap form control styling
- Strength validation via Django's password validators

---

### Data Model

#### **CustomUser**

Extended user model with image processing and custom validators.

```python
class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(name='username', verbose_name='Username', unique=True,
                                validators=[UnicodeUsernameValidator],
                                max_length=50, null=True)
    email = models.EmailField(name='email', verbose_name='Email', max_length=254,
                              validators=[validate_email], null=True)
    password = models.CharField(name='password', verbose_name='Password', max_length=20, 
                               validators=[validate_password], null=True)
    photo = models.ImageField(name='photo', verbose_name='Photo', default='default_account_picture.jpg',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg'],
                                                                 message='Your Photo Don\'t have allowed extension')],
                              upload_to='user_photo',
                              null=True,
                              blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_photo(self):
        return self.photo.url

    def get_absolute_url(self):
        return reverse(viewname='authorization_user', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
```

**Fields**:
- **username**: Unique, unicode validator, max 50 chars
- **email**: RFC-validated, max 254 chars
- **password**: Hashed password, max 20 chars
- **photo**: JPG ImageField, auto-resizes to 300x300px

**Methods**:
- `get_photo()`: Returns media URL for template rendering
- `get_absolute_url()`: Returns profile URL for redirects
- `save()`: Auto-resize uploaded images using Pillow
  - Checks if image height/width exceeds 300px
  - Creates 300x300 thumbnail
  - Overwrites original file with resized version

---

## Project Structure

```
MyWebSite/
├── MyWebSite/          # Django project configuration
├── authorization_user/ # User authentication app
│   ├── views.py        # CreateUserView, LoginUserView, UserDetailView, ChangeUserPasswordView, UserLogoutView
│   ├── forms.py        # RegistrationUserForm, LoginUserForm, ChangeUserPasswordForm
│   ├── models.py       # CustomUser model with image processing
│   ├── urls.py         # Authentication URL routing
│   ├── utils.py        # AuthorizationUserMixin
│   └── admin.py        # Django admin configuration
├── main/               # Main application
│   ├── views.py        # HomeView with calendar functionality
│   ├── urls.py         # Main URL routing
│   └── utils.py        # HomeMixin
├── templates/
│   ├── base.html                    # Base template with block inheritance
│   ├── authentication_user/
│   │   ├── login_user.html          # Login form
│   │   ├── registration_user.html   # Registration form
│   │   ├── change_password.html     # Password update
│   │   └── user_profile.html        # User profile view
│   └── includes/
│       ├── default_navbar.html      # Unauthenticated navigation
│       ├── auth_user_navbar.html    # Authenticated navigation
│       └── message.html             # Flash message display
├── static/
│   ├── main/
│   │   ├── css/styles.css           # Grayscale theme stylesheet (246KB)
│   │   ├── js/scripts.js            # Core JavaScript utilities
│   │   ├── icon/                    # Favicon assets
│   │   └── img/                     # Theme images (ipad.png, demo images)
│   └── authentication_user/
│       ├── css/                     # Auth-specific styles
│       └── js/                      # Auth-specific scripts
├── media/
│   └── user_photo/                  # User-uploaded profile photos
├── manage.py           # Django management utility
└── db.sqlite3          # SQLite database
```

## Author

[Mihai Apostol](https://github.com/mihaiapostol14)

## License

No license specified. If you plan to share or reuse this project, add a LICENSE file (for example, MIT) to clarify terms.