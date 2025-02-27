from django.shortcuts import render
from .models import VideoPromotion


def video_slider(request):
    videos = VideoPromotion.objects.all()
    # return render(request, 'shop_app/home.html', {'videos': videos})
    return render(request, 'shop_app/embedvideo.html', {'videos': videos})
