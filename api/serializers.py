from rest_framework import serializers
from api.models.post import Blog
from api.models.deleted_log import DeletedLog
from api.models.updated_log import LogUpdated
# chuyển queryset or models thành dạng dữ liệu dễ dàng render trên web cụ thể là json/xml
# chuyển json/xml của client chuyển lên thành object để django xử lí    
class BlogSerializer(serializers.ModelSerializer):
    is_deleted = serializers.SerializerMethodField()
  #Ở đây là model Blog gồm các trường ('id', 'title', 'content', 'description', 'created_at','author')
  #  created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Blog
        fields = ['id', 'title','description', 'content','author' ,'created_at','updated_at', 'deleted_at', 'is_deleted','is_published']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']    
    def get_is_deleted(self, obj):
        return obj.deleted_at is not None  
class BlogSerializers(serializers.ModelSerializer):
    #is_deleted là một trường ảo, không có trong model Blog và không có trong cơ sở dữ liệu
    is_deleted = serializers.SerializerMethodField()
    class Meta:
        model = Blog
      #  fields = ('id', 'title', 'description', 'created_at', 'author','deleted_at')
        fields = ['id', 'title', 'content','author' ,'created_at','updated_at', 'deleted_at', 'is_deleted','is_published']
      # chỉ được đọc không được chỉnh sửa       
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at'] 
    def get_is_deleted(self, obj):
          return obj.deleted_at is not None  
    
class DeletedLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeletedLog
        fields = ['id','action','time', 'deleted_by', 'restored_by', 'post_id']
class LogUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogUpdated
        fields = ['id', 'post', 'action', 'time', 'updated_fields', 'old_value', 'new_value', 'updated_at', 'updated_by']