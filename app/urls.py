from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path("category/<slug:val>", views.CategoryView.as_view(), name='category'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)