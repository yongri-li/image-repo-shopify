from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.


class User(AbstractUser):
    pass

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    author = models.ForeignKey(User,on_delete=CASCADE,default=None,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"{self.title}"