from django.db import models

class InputText(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)