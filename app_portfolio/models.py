
from django.db import models


class PortfolioUser(models.Model):
    user = models.ForeignKey('app_user.UserProfile', on_delete=models.CASCADE, related_name="port_media")  # kaitkan ke user
    deskripsi = models.TextField(blank=True, null=True)
    skill = models.CharField(max_length=255, blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    portfolio_link = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name or self.user.email