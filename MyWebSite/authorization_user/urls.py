from django.urls import path
from . import views

app_name = 'authorization_user'

urlpatterns = [
    path('registration-user/', views.CreateUserView.as_view(), name='registration-user'),
    path('user-profile/<int:pk>', views.UserDetailView.as_view(), name='user-profile'),
    path('login-user/', views.LoginUserView.as_view(), name='login-user'),
    path('change-password/', views.ChangeUserPasswordView.as_view(), name='change-password'),
    path('logout-user/', views.UserLogoutView.as_view(), name='logout-user'),
]