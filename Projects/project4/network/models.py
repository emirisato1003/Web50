from django.contrib.auth.models import AbstractUser
from django.db import models

# bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
#     following = models.ManyToManyField(User, symmetrical=False, related_name='following')
#     follower = models.ManyToManyField(User, symmetrical=True, related_name='follower')

class User(AbstractUser):
    pass

class Posts(models.Model):
    post = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post} on {self.date_posted} by {self.user}. Likes: {self.like}"

class Follow(models.Model):
    user_following = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follower')

    def __str__(self):
        return f"{self.user_following} is following {self.follower}"

class Like(models.Model):
    user_like = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='user_like') 
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True, related_name='post_like')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_like} likes {self.post.post} posted by {self.post.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_post")
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment