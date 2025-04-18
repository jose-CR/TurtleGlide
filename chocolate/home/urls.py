from django.urls import path
from .views import app, Profile, ProfileCreateView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('', app, name="app"),
    path('logout', Profile.exit, name="exit"),
    # CRUD Profile
    path('register/', ProfileCreateView.as_view(), name='register'),
    path('profile/', Profile.index ,name="profile"),
    path('profile/edit/<int:pk>', ProfileUpdateView.as_view() , name="profile_edit"),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view() , name="profile_delete")
]