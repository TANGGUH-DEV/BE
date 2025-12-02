from django.db import models
import uuid
from django.utils.text import slugify



class News(models.Model):
    CATEGORY_CHOICES = [
        ("national", "Nasional"),
        ("international", "Internasional"),
        ("technology", "Teknologi"),
        ("entertainment", "Hiburan"),
    ]

    author = models.ForeignKey('app_user.UserProfile', on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)  # URL-friendly title
    content = models.TextField(null= True, blank=True)  # isi utama berita
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.URLField(blank=True, null=True)  # bisa dari Media juga
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str (uuid.uuid4())[:8] #potong biar penedek
            self.slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title
