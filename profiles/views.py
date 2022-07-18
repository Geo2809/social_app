from django.views.generic import ListView
from django.shortcuts import redirect, render
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.contrib.auth import get_user_model

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


