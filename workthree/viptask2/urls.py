# django_app/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from five.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout_page'),
    path('user-view/', user_view, name='user_view'),
    path('radiologist_view/', radiologist_view, name='radiologist_view'),  # Add this line

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
