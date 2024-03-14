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
    path('radiologist_view/', radiologist_view, name='radiologist_view'),
    path('surgeon_view/', surgeon_view, name='surgeon_view'),
    path('teleradiologist_view/', teleradiologist_view, name='teleradiologist_view'),
    path('start_process/', start_process, name='start_process'),
    path('step1/<uuid:record_id>/', step1_view, name='step1_view'),
    path('step2/<uuid:record_id>/', step2_view, name='step2_view'),
    path('step3/<uuid:record_id>/', step3_view, name='step3_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
