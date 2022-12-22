from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatar/%y/%m/%d/", default='default.png')
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=125)
    bio = models.TextField(max_length=150)
    telegram = models.URLField(max_length=200, blank=True, null=True, default='#')
    instagram = models.URLField(max_length=200, blank=True, null=True, default='#')
    website = models.URLField(max_length=200, blank=True, null=True, default='#')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    total_likes = models.IntegerField(default=0)
    total_works = models.IntegerField(default=0)

    USERNAME_FIELD = "username"
    first_name = None
    last_name = None

    def __str__(self):
        return f"{self.username} - {self.created_at}"
    
    def get_absolute_url(self):
        return reverse('account:profile', kwargs={'username': self.username})

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"
