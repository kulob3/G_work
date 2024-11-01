from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, password_reset_request, UserListView, ban_user, unban_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('', UserListView.as_view(), name='user_list'),
    path('ban/<int:user_id>/', ban_user, name='ban_user'),
    path('unban/<int:user_id>/', unban_user, name='unban_user'),
]