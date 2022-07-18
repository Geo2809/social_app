from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles-view'),
]