from django.db import models
from api.models.post import Blog
import django.utils.timezone as timezone
# CREATE TABLE deleted_log (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     deleted_at datetime NOT NULL ,
#     restored_at datetime NULL DEFAULT NULL,
#     deleted_by VARCHAR(45),
#     restored_by VARCHAR(45) NULL DEFAULT NULL
# )
# 

    
class DeletedLog(models.Model):
    class Meta : 
        db_table = 'log'
    ACTION_CHOICES = (
        ('deleted', 'Deleted'),
        ('restored', 'Restored'),

        )

    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(choices=ACTION_CHOICES,max_length=100)
    time = models.DateTimeField(default=timezone.now)
    # restored_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=45)
    restored_by = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"{self.action.capitalize()} post {self.post.id} at {self.deleted_at}"