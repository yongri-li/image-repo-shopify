from images.models import Image
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('register/',views.register_view,name="register"),
    path('upload/',views.upload_view,name="upload"),
    path('bulk-upload/',views.bulk_upload_view,name="bulk-upload"),
    path('images/<str:level>',views.images,name="images"),
    path('create',views.create_view,name="create"),
    path('test/',views.test,name="test")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)