from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.urls import reverse
class CustomUser(AbstractUser):
    pass


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_profiles_available(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.sender)
                accepted.add(rel.receiver)
        available = [profile for profile in profiles if profile not in accepted]
        return available


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(blank=True)
    country = CountryField()
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})
         
    def get_friends(self):
        return self.friends.all()

    def get_number_of_friends(self):
        return self.friends.all().count()

    def get_all_posts(self):
        return self.posts.all()

    def get_number_of_posts(self):
        return self.posts.all().count()

    def get_number_of_received_likes(self):
        posts = self.posts.all()
        total_likes = 0
        for item in posts:
            total_likes += item.liked.all().count()
        return total_likes

    def get_number_of_given_likes(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1       
        return total_liked
        

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name}"

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.slug = slugify(f'{self.first_name} - {self.last_name} - {self.user.id}')
        else:
            self.slug = slugify(f'{self.user} - {self.user.id}')
        return super(Profile, self).save(*args, **kwargs)


SEND_CHOICE = 'send'
ACCEPTED_CHOICE = 'accepted'

STATUS_CHOICES = [
    (SEND_CHOICE, 'send'),
    (ACCEPTED_CHOICE, 'accepted')
]

class RelationshipManager(models.Manager):
    def friend_requests_received(self, receiver):
        requests_received = Relationship.objects.filter(receiver=receiver, status='send')
        return requests_received


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return f'{self.sender} - {self.receiver} - {self.status}'