from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('my-friend-requests/', views.friend_requests_received_view, name='friend-requests-received-view'),
    path('available-profiles', views.available_profiles_list_view, name='available-profiles-view'),
    path('send-friend-request/', views.send_friend_request_view, name='send-friend-request-view'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend-view'),
    path('my-friend-requests/accept/', views.accept_friend_request, name='accept-friend-request-view'),
    path('my-friend-requests/reject/', views.reject_friend_request, name='reject-friend-request-view'),
]