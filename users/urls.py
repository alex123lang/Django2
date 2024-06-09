from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from users.apps import UsersConfig
from users.views import UserCreateView, email_verify

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-verify/<str:token>/', email_verify, name='email_verify'),
    path('password-reset/',
         PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                   email_template_name='users/password_reset_email.html',
                                   success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]
