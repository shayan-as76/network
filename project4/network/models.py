from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    content = models.TextField(verbose_name='post')
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    like = models.IntegerField(default=0, verbose_name='like')

    def __str__(self):
        return self.content


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}/{self.user}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_is_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_is_being_followed")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"