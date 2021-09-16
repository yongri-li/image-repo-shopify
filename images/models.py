from typing import Callable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.


class User(AbstractUser):
    pass

class Repo(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=CASCADE,default=None,null=True,blank=True)
    private = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="images",default=None)

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "title":self.title,
            "timestamp":self.timestamp,
            "author":self.author.username,
            "private":self.private,
            "description":self.description,
            "thumbnail":self.thumbnail.url
        }


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    repo = models.ForeignKey(Repo,on_delete=CASCADE,default=None,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=CASCADE,default=None,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "title":self.title,
            "image":self.image.url,
            "author":self.author.username,
            "timestamp":self.timestamp,
            "private":self.private
        }