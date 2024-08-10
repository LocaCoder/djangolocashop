from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('verify/', views.UserVerifyView.as_view(), name='user_verify'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('password_reset/', views.UserResetPasswordView.as_view(), name='password_reset'),
    path('password_change/', views.UserChangePasswordView.as_view(), name='password_change'),
]