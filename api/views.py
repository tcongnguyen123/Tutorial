from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from api.models.post import Blog
from api.models.deleted_log import DeletedLog
from api.models.updated_log import LogUpdated
from .serializers import BlogSerializer,DeletedLogSerializer,LogUpdatedSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from .pagination import StandardPagination
from copy import deepcopy
# Create your views here.
# test hello world
class TestView(ViewSet):
    def post_test(self, request):
        data = {
            "name": "Hello world"
        }
        return Response(data)

class BlogViewSet(ViewSet):
    # lấy post theo id
    def get_blog_id(self,request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    # lấy tất cả post(blog)    
    def list(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    #thêm post mới với nháp (chưa được public)
    def create(request):
        serializer = BlogSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save(is_published=False)
            return Response({'Post has been created.'},serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # public post 
    def publish_post(self,request, pk_1): # nhận vào req và khóa
        try:
            blog = Blog.objects.get(pk=pk_1)   # lấy dữ liệu theo khóa
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #nêu is_deleted = true thì không cho public
        if blog.deleted_at is not None:
            return Response({'Post has been deleted.'}, status=status.HTTP_400_BAD_REQUEST)

        # Cập nhật bài viết để xuất bản
        blog.is_published = True
        blog.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #unpublic post
    def unpublic_post(self,request, pk): # nhận vào req và khóa
        try:
            blog = Blog.objects.get(pk=pk)   # lấy dữ liệu theo khóa
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #nêu is_published = true thì không cho public
        if blog.is_published == True:
            blog.is_published = False
            blog.save()
            return Response({'Post no public.'},status=status.HTTP_204_NO_CONTENT)
        

    # sort mới đến cũ
    def sort_blogs_by_date(self,request):
        blogs = Blog.objects.all().order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    # phân trang
    def page(self, request, *args, **kwargs):
        queryset = Blog.objects.all()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BlogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

        serializer = BlogSerializer(queryset,many=True)
        return Response(serializer.data)
    # xóa tạm 1 post bằng id

    def delete_blog_temp(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        blog.deleted_at = timezone.now()
        blog.save()

        # Lưu log khi xóa mềm
        #Sau này đổi thành người xóa , bây giờ để tác giả là người xóa
        DeletedLog.objects.create(post=blog, action='deleted', deleted_by= blog.author)

        return Response(status=status.HTTP_204_NO_CONTENT)
    def restore_blog(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        blog.deleted_at = None
        blog.save()
        DeletedLog.objects.create(post=blog, action='restored', restored_by=blog.author)
        return Response(status=status.HTTP_204_NO_CONTENT)
    # xóa 1 post bằng id vĩnh viễn
    def destroy_blog(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if blog.deleted_at is not None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Bài viết đã bị xóa trước đó'})
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # tìm kiếm post theo author
    def search_blog_by_author(self, request, author):
        blogs = Blog.objects.filter(author__icontains=author)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    #   tìm kiếm post theo title
    def search_blog_by_title(self, request, title):
        blogs = Blog.objects.filter(title__icontains=title)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    # tìm kiếm post theo content
    def search_blog_by_content(self, request, content):
        blogs = Blog.objects.filter(content__icontains=content)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    #sort theo title
    def sort_blogs_by_title(self, request):
        blogs = Blog.objects.all().order_by('title')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    # lấy deleted log theo post
    def get_deleted_log_by_post(self, request, pk):
        deleted_logs = DeletedLog.objects.filter(post=pk)
        serializer = DeletedLogSerializer(deleted_logs, many=True)
        return Response(serializer.data)
    def get_updated_log_by_post(self, request, pk):
        updated_logs = LogUpdated.objects.filter(post=pk)
        serializer = LogUpdatedSerializer(updated_logs, many=True)
        return Response(serializer.data)
    

    # update 1 post bằng id
    
    def update(self, request, blog_id):
        # 161-164: Lấy đối tượng Blog từ database theo id bằng phương thức get()
        # nếu không thì trả về 404  
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Copy the current state of the blog object
        # Tạo bản sao để lưu lại trạng thái trước khi update
        current_state = deepcopy(blog)
        # Chuyển đổi dữ liệu từ request.data thành blog object
        serializer = BlogSerializer(blog, data=request.data)
        # kiểm tra xem dữ liệu có hợp lệ không
        if serializer.is_valid():
            # danh sách các trường được update
            updated_fields = []
            # dict chứa giá trị cũ của các trường được update
            old_value = {}
            # dict chứa giá trị mới của các trường được update
            new_value = {}
            # key là tên trường, value là giá trị của trường
            # serializer.validated_data là dict chứa dữ liệu đã được validate bao gồm id, title, content, author 
            for key, value in serializer.validated_data.items():
                # getattr(blog, key) là giá trị của trường key trong đối tượng blog
                # value là giá trị của trường key trong request.data
                if getattr(blog, key) != value:
                    # nếu giá trị của trường key trong đối tượng blog khác với giá trị của trường key trong request.data
                    if key not in updated_fields:
                        # nếu key được update thì thêm vào updated_fields
                        updated_fields.append(key)
                        # lưu giá trị cũ và giá trị mới của trường key
                        old_value[key] = getattr(current_state, key)
                        new_value[key] = value

            serializer.save()
            # tạo log khi update gồm các trường được update, giá trị cũ và giá trị mới và id của post
            LogUpdated.objects.create(
                post=blog,
                action='updated',
                updated_fields=updated_fields,
                old_value=old_value,
                new_value=new_value,
                # updated_by=request.user.username,
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# hàm CRUD cho comment
    
    # sự khác biệt với hàm update là hàm này chỉ update 1 phần của post
    # nếu update 1 phần thì sẽ có 1 trường updated_fields là 1 list các trường đã được update
    # nếu update toàn bộ thì sẽ không có trường updated_fields
    # nhưng def update thì có trường updated_fields luôn vì nó update toàn bộ



# Sự khác biệt thứ ba giữa hai đoạn code đó là cách mà họ tạo ra các thông tin cập nhật cho bản ghi Blog.

# Trong đoạn code thứ nhất, sau khi thực hiện lưu thông tin cập nhật vào đối tượng Blog, một vòng lặp được sử dụng để kiểm tra tất cả các trường của bản ghi Blog (bằng cách
# lặp qua các khóa của hai bản sao khác nhau của đối tượng Serializer). Khi tìm thấy một trường đã thay đổi, đối tượng LogUpdated được tạo ra để ghi lại thông tin
# về trường đã được cập nhật.

# Trong đoạn code thứ hai, một cách tiếp cận khác được sử dụng. Thay vì lặp qua các trường và kiểm tra xem chúng có thay đổi hay không, đoạn code này so sánh các giá 
# trị mới và cũ của tất cả các trường được truyền vào Serializer. Nếu giá trị của một trường đã thay đổi, một mục nhập được thêm vào danh sách các trường được cập nhật 
# và các giá trị cũ và mới của trường đó được lưu trữ trong các từ điển riêng biệt. Sau đó, thông tin được lưu trữ vào bảng LogUpdated với các giá trị này.

# Về mặt logic, hai đoạn code này là tương đương nhau, tuy nhiên cách tiếp cận của chúng khác nhau. Đoạn code thứ hai có thể tối ưu hơn trong trường hợp bản ghi 
# có nhiều trường, vì nó không lặp lại việc truy cập đối tượng Serializer và Blog. Tuy nhiên, đoạn code thứ nhất có thể dễ hiểu hơn đối với một số lập trình viên, 
# vì nó sử dụng một vòng lặp rõ ràng để kiểm tra từng trường của đối tượng.


################################################ GHI CHÚ OR 1 SỐ CÁI KHÁC #############################################################
#### DECORATOR @API_VIEW ###### 
# # Class-based Views
# #lấy danh sách các post
# # xác định phương thức HTTP được dùng
# @api_view(['GET'])
# def get_blogs(request): # nhận request
#     blogs = Blog.objects.all() # lấy tất cả đối tượng từ CSDL
#     serializer = BlogSerializers(blogs, many=True) # đổi thành dạng json với đối tượng là blog ,"many" serialize nhiều đối tượng
#     return Response(serializer.data) # trả về client data đã có 

# # thêm post mới
# @api_view(['POST'])
# def create_blog(request):
#     serializer = BlogSerializer(data=request.data)    
#     if serializer.is_valid():# kiểm tra data có hợp lệ không
#         serializer.save(is_published=False)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Nếu serializer không hợp lệ, view function sẽ trả về lỗi và HTTP status code 400 Bad Request.
# #public  post 
# @api_view(['PUT'])
# def publish_post(request, id):
#     try:
#         Blog = Blog.objects.get(pk=id)
#     except Blog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # Cập nhật bài viết để xuất bản
#     Blog.is_published = True
#     Blog.save()

#     return Response(status=status.HTTP_204_NO_CONTENT)
# # lấy 1 post theo id
# @api_view(['GET'])
# def get_blog(request, pk):
#     try:
#         blog = Blog.objects.get(pk=pk)
#     except Blog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = BlogSerializer(blog)
#     return Response(serializer.data)

# # cập nhật 1 post bằng id

# @api_view(['PUT'])
# def update_blog(request, pk): # nhận vào req và khóa
#     try:
#         blog = Blog.objects.get(pk=pk)   # lấy dữ liệu theo khóa
#     except Blog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = BlogSerializer(blog, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # xóa 1 post bằng id
# @api_view(['DELETE'])
# def delete_blog(request, pk):
#     try:
#         blog = Blog.objects.get(pk=pk)
#     except Blog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     blog.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# #sort mới đến cũ
# @api_view(['GET'])
# def sort_blogs_by_date(request):
#     blogs = Blog.objects.all().order_by('-created_at')
#     serializer = BlogSerializer(blogs, many=True)
#     return Response(serializer.data)

################### hết dùng decorator api_view #############################
#dùng viewset 
# Blog.DoesNotExist: kiểm tra xem có trong CSDL không
# serializer.is_valid() : kiểm tra xem data có hợp lệ không
# status là một module trong rest_framework, nó chứa các HTTP status code, chúng ta có thể sử dụng để trả về cho client.
# lấy tất cả post(blog) theo id   
    # post=blog: đây là một trường hợp của mối quan hệ một-nhiều giữa bảng DeletedLog 
    # và bảng Blog được thiết lập thông qua trường ForeignKey. Trong đó post là một tham
    #  chiếu đến một bản ghi trong bảng Blog, và blog là đối tượng Blog được truyền vào qua tham số
    #  của hàm. Điều này cho phép lưu trữ thông tin về bài đăng liên quan đến nhật ký xóa mềm.
    #  DeletedLog.objects.create(post=blog, action='deleted', deleted_by= blog.author)
    #nên tạo deleted log chung với updated log không ?
    # def create_deleted_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     DeletedLog.objects.create(post=blog, action='deleted', deleted_by= blog.author)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    # def create_restored_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     DeletedLog.objects.create(post=blog, action='restored', restored_by=request.author)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def create_updated_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     UpdatedLog.objects.create(post=blog, action='updated', updated_by= blog.author)
        # post=blog: đây là một trường hợp của mối quan hệ một-nhiều giữa bảng DeletedLog 
    # và bảng Blog được thiết lập thông qua trường ForeignKey. Trong đó post là một tham
    #  chiếu đến một bản ghi trong bảng Blog, và blog là đối tượng Blog được truyền vào qua tham số
    #  của hàm. Điều này cho phép lưu trữ thông tin về bài đăng liên quan đến nhật ký xóa mềm.
    #  DeletedLog.objects.create(post=blog, action='deleted', deleted_by= blog.author)
    #nên tạo deleted log chung với updated log không ?
    # def create_deleted_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     DeletedLog.objects.create(post=blog, action='deleted', deleted_by= blog.author)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    # def create_restored_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     DeletedLog.objects.create(post=blog, action='restored', restored_by=request.author)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def create_updated_log(self, request, id):
    #     try:
    #         blog = Blog.objects.get(id=id)
    #     except Blog.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     UpdatedLog.objects.create(post=blog, action='updated', updated_by= blog.author)
        # lấy delete log
    # def get_deleted_log(self, request,pk):
    #     deleted_logs = DeletedLog.objects.all()
    #     serializer = DeletedLogSerializer(deleted_logs, many=True)
    #     return Response(serializer.data)