from django.db import models


class UserProfile(models.Model):
    class role (models.TextChoices):
        USER = "USER", "user"
        ADMIN =  "ADMIN", "admin"
        SUPERADMIN = "SUPERADMIN", "superadmin"

   

    uid = models.CharField(max_length=128, unique=True)  # UID dari Firebase\
    role = models.CharField( max_length=20, choices=role.choices, default=role.USER)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.email



