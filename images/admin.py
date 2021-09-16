from images.models import Image
from django.contrib import admin
from .models import Repo, User, Image
# Register your models here.

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Repo)
