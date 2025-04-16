from django.urls import path
from . import views
from .auth.password import PasswordViews

urlpatterns = [
    path('', views.app, name='app'),
    path('logout/', views.exit, name='exit'),
    path('register/', views.register, name='register'),

    # vistas profiles
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', PasswordViews.Change.as_view(), name="change-password"),
    path('profile/reset-password/', PasswordViews.Reset.as_view(), name="reset-password"),
    path('profile/<uidb64>/<token>/', PasswordViews.Confirm.as_view(), name="reset-password-confirm"),
    path('profile/reset/complete', PasswordViews.Complete.as_view(), name="reset-password-done"),
]
