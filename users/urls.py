from django.contrib import admin
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    # profileのpkです
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),

    # profileのpkです
    path('username_change/<int:pk>/', views.UserNameChange.as_view(), name='username_change'),
    path('profile_change/<int:pk>/', views.ProfileChange.as_view(), name='profile_change'),
    path('account_delete/', views.AccountDelete.as_view(), name='delete_account'),
    path('user_config/', views.UserConfig.as_view(), name='user_config'),
    path('terms_of_service/', views.TermsOfService.as_view(), name='terms_of_service'),
    path('privacy_policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),

]
