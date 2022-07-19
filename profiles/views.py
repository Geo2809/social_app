from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from .forms import ProfileModelForm
from .models import Profile, Relationship

User = get_user_model()

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if form.is_valid():
        form.save()
        confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/myprofile.html', context)





class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profiles = Profile.objects.get_all_profiles(self.request.user)
        return profiles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for rel in rel_r:
            rel_receiver.append(rel.receiver.user)
        for rel in rel_s:
            rel_sender.append(rel.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        print(rel_sender)
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

def friend_requests_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.friend_requests_received(profile)
    results = [x.sender for x in qs]
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs': results,
        'is_empty': is_empty
    }
    return render(request, 'profiles/friend_requests_received.html', context)

def accept_friend_request(request):
    if request.method == 'POST':
        sender = Profile.objects.get(pk=request.POST.get('profile_pk'))
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()
    return redirect('profiles:friend-requests-received-view')

def reject_friend_request(request):
    if request.method == 'POST':
        sender = Profile.objects.get(pk=request.POST.get('profile_pk'))
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()
    return redirect('profiles:friend-requests-received-view')  

def available_profiles_list_view(request):
    user = request.user
    profiles = Profile.objects.get_all_profiles_available(user)
    
    context = {
        'profiles': profiles
    }
    return render(request, 'profiles/available_profiles_list.html', context) 

def send_friend_request_view(request):
    if request.method == 'POST':
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=request.POST.get('profile_pk'))
        Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


def remove_from_friends(request):
    if request.method == 'POST':
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=request.POST.get('profile_pk'))

        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
        