from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass


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

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.slug = slugify(f'{self.first_name} - {self.last_name} - {self.user.id}')
        else:
            self.slug = slugify(f'{self.user} - {self.user.id}')
        return super(Profile, self).save(*args, **kwargs)