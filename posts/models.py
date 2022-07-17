from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.content[:20]}- {self.author.first_name}'

    
    def number_of_likes(self):
        return self.liked.all().count()


    def number_of_comments(self):
        return self.comment_set.all()

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.body}'

LIKE_CHOICE = 'Like'
UNLIKE_CHOICE = 'UnLike'
VALUE_CHOICES = [
    (LIKE_CHOICE, 'Like'),
    (UNLIKE_CHOICE, 'UnLike'),
]

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=6, choices=VALUE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.post} - {self.value}'