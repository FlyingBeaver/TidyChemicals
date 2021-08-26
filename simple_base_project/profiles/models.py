from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="smiling_cat.gif",
                                        upload_to="uploads/")

    def __str__(self):
        return self.user.username
