
from django.db import models



class Media(models.Model):
    MEDIA_TYPES = [
        ("image", "Image"),
        ("video", "Video"),
        ("audio", "Audio"),
    ]

    user = models.ForeignKey('app_user.UserProfile', on_delete=models.CASCADE,related_name="media_media")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField()  # Simpan URL file yang diupload
    media_type = models.CharField(max_length=50, choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} ({self.user.email})"
