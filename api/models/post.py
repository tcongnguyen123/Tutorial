from django.db import models

class Blog(models.Model):
    
    class Meta : 
        # kết nối với bảng post trong cơ sở dữ liệu 
        db_table = 'post'
    # các bài post gồm các thuộc tính sau (title, content. descripton, created_at, author và updated_at(bài này chưa tạo))
    title = models.CharField(max_length=255)
    content = models.TextField()    
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

# class Draft(models.Model):
#     class Meta : 
#         # kết nối với bảng post trong cơ sở dữ liệu 
#         db_table = 'post'
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

