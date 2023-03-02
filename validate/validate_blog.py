from rest_framework import serializers
from api.serializers import BlogSerializer 
from api.models.post import Blog
class IdGetUserValidate(serializers.Serializer):
    def is_deleted(blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
            return blog.deleted_at is not None
        except Blog.DoesNotExist:
            return True