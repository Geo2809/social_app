from profiles.models import Profile, Relationship
def number_of_friend_requests_received(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        nr_of_requests = Relationship.objects.friend_requests_received(profile).count()
        return {'nr_of_requests': nr_of_requests}
