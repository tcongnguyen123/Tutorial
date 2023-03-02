from django.db import models
from api.models.post import Blog
import django.utils.timezone as timezone
class LogUpdated(models.Model):
    class Meta:
        db_table = 'log_updated'
        

    ACTION_CHOICES = (
        ('updated', 'Updated'),
        ('created', 'Created'),
    )
    post = models.ForeignKey('Blog', on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION_CHOICES, max_length=100)
    time = models.DateTimeField(default=timezone.now)

    updated_fields = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=45)