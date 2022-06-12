from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    avatar = models.IntegerField(default=0)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blogImages")
    areCommentsAllowed = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.FloatField()
    time = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)
    initials = models.CharField(max_length=3, null=True, blank=True)


"""
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(blogPost, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

"""