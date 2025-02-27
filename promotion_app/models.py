from django.db import models
from embed_video.fields import EmbedVideoField
import re


class VideoPromotion(models.Model):
    title = models.CharField(max_length=255)
    full_video_url = models.URLField(help_text="Paste Facebook, YouTube, or Google Drive video link")

    youtube_video_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    facebook_video_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    google_drive_video_id = models.CharField(max_length=100, blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        url = self.full_video_url.strip()  # ✅ বাড়তি স্পেস থাকলে রিমুভ করা

        # 🔹 Facebook Video ID Processing (Facebook আগে চেক করবো)
        if "facebook.com" in url or "fb.watch" in url:
            fb_match = re.search(r"(?:/videos/|v=|fb.watch/)([\dA-Za-z_-]+)", url)
            if fb_match:
                self.facebook_video_id = fb_match.group(1)

        # 🔹 Google Drive Video ID Processing (Google Drive ২য় চেক)
        elif "drive.google.com" in url:  # ✅ Google Drive-এর ডোমেইন চেক
            drive_match = re.search(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)", url)
            if drive_match:
                self.google_drive_video_id = drive_match.group(1)

        # 🔹 YouTube Link Processing (সবশেষে YouTube চেক করবো)
        elif "youtube.com" in url or "youtu.be" in url:  # ✅ YouTube-এর ডোমেইন চেক
            youtube_match = re.search(r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]+)", url)
            if youtube_match:
                self.youtube_video_id = youtube_match.group(1)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

