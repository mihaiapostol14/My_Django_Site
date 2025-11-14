from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    login
)
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView
)

from .forms import (
    RegistrationUserForm,
    LoginUserForm,
    ChangeUserPasswordForm
)
from .utils import AuthorizationUserMixin

User = get_user_model()


class CreateUserView(CreateView,AuthorizationUserMixin):
    template_name = 'authentication_user/registration_user.html'
    form_class = RegistrationUserForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        login(self.request,user=self.object,backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Django already handles rendering the form with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Registration User')

    def get_success_url(self):
        messages.success(request=self.request, message=f'Registration {self.request.user} Successful')
        return reverse_lazy('authentication_user:user-profile',kwargs={'pk':self.request.user.pk})



class LoginUserView(AuthorizationUserMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication_user/login_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Login User')

    def get_success_url(self):
        messages.success(request=self.request, message=f'Login {self.request.user} Successful')
        return reverse_lazy('authorization_user:user-profile', kwargs={'pk':self.request.user.pk})


class UserDetailView(AuthorizationUserMixin, DetailView):
    model = User
    template_name = 'authentication_user/user_profile.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)


class ChangeUserPasswordView(AuthorizationUserMixin, PasswordChangeView):
    template_name = 'authentication_user/change_password.html'
    form_class = ChangeUserPasswordForm

    def get_success_url(self):
        messages.success(request=self.request, message=f'Change Password {self.request.user} Successful')
        return reverse_lazy('authentication_user:user-profile',kwargs={'pk':self.request.user.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)


class UserLogoutView(LogoutView, AuthorizationUserMixin):  # TODO: UserLogoutView
    http_method_names = ["post", "get"]
    template_name = 'authentication_user/logout_user.html'

    def get_success_url(self):
        return reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Logout {self.request.user}')