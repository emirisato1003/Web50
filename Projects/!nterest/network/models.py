from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    post = models.ImageField(upload_to='image',null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, related_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    like = models.IntegerField(default=0)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_like')
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} like {self.post.title}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_profile')
    icon_img = models.ImageField(upload_to='icon', null=True, blank=True)
    profile_img = models.ImageField(upload_to='profile', null=True, blank=True)

class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follower')

    def __str__(self):
        return f"{self.user_following} is follow {self.follower}"

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_save')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_save')
    is_save = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} save {self.post.title}"