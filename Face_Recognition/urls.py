from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name="Index"),
    path('admin/', views.admin, name="admin"),
    path('data', views.get_data, name="data"),
    path('webcam', views.webcam_feed, name="webcam"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)