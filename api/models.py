import binascii
import os

from django.db import models

from rest_framework.authtoken.models import Token

from django.conf import settings


class Task(models.Model):
    title = models.CharField(max_length=120)
    action = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class CustomToken(models.Model):
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='custom_token',
        on_delete=models.CASCADE, null=True,
        blank=True
    )
    created = models.DateTimeField("Created", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
