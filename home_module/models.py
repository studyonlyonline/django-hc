from django.db import models

# Create your models here.
class Schemes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(default=None)
    title = models.CharField(max_length=255)
    terms_and_conditions = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
