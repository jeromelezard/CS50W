from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Post(models.Model):
    content = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    likes = models.ManyToManyField(User, related_name="post")
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
    def __str__(self):
        return self.content
class Following(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    
    def __str__(self):
        return f"{self.from_user.username} is following:"
    def serialize(self):
        return {
            "user": self.from_user.username,
            "is_following": [user.username for user in self.following.all()]
        }

