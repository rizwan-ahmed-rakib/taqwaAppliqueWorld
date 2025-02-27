from django.urls import path
from .views import video_slider

urlpatterns = [
    path('videos/', video_slider, name='video_slider'),
]