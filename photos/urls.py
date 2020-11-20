from django.urls import path

from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('get', views.get, name='get'),
    path('share', views.share, name='share'),
    path('getImage', views.getImage, name='getImage'),
    path('getSharedImages', views.getSharedImages, name="getSharedImages"),
    path('annotate', views.annotate, name="annotate"),
    path('getAnnotations', views.getAnnotations, name="getAnnotations"),
    path('getAnnotatedThumbnails', views.getAnnotatedThumbnails, name="getAnnotatedThumbnails"),
]
