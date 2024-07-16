from django.db import models

class User(models.Model):
    
    class Meta : 
        # kết nối với bảng post trong cơ sở dữ liệu 
        db_table = 'user'
    # các bài post gồm các thuộc tính sau (title, content. descripton, created_at, author và updated_at(bài này chưa tạo))
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.username