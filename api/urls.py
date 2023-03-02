from django.contrib import admin
from django.urls import path
from .views import BlogViewSet
from . import views


urlpatterns = [
    # #them 1 post
    # path('post_test', TestView.as_view({'post':'post_test'}), name='post_test'),
    # #public 1 post
    # path('posts/<int:post_id>/publish/', views.publish_post, name='publish_post'),
    # # lấy tất cả các post
    # path('blogs/', views.get_blogs, name='get_blogs'),
    # # lấy post theo id
    # path('blogs/<int:pk>/', views.get_blog, name='get_blog'),
    # path('blogs/create/', views.create_blog, name='create_blog'),
    # # cập nhật post theo id
    # path('blogs/<int:pk>/update/', views.update_blog, name='update_blog'),
    # # xóa post theo id
    # path('blogs/<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    # # sắp xếp từ mới đến cũ
    # path('blogs/sort_by_date/', views.sort_blogs_by_date, name='sort_blogs_by_date'),
    # #viewset
    # #lấy tất cả post 
    # path('blogs/get', Test_GetBlog.as_view({'get':'list'}), name='list'),
    # # lấy post theo id
    # path('blogs/get/<int:pk>/', Test_GetBlog.as_view({'get':'get_blog'}), name='get_blog'),
    # #phân trnag
    # #http://localhost:8000/blogs/page/1?page=3
#     # http://localhost:8000/blogs/page/1?page=1
#     path('blogs/page/<int:pk>', BlogViewSets.as_view({'get':'page'}), name='page'),
    
    
    

    # path('blogs/', blog_list, name='blog_list'),
    # path('blogs/<int:pk>/', blog_detail, name='blog_detail'),
    path('blogs/', BlogViewSet.as_view({'get': 'list'}), name='list'),
    path('blogs/<int:pk>/', BlogViewSet.as_view({'get': 'get_blog_id'}), name='get_blog_id'),
    path('blogs/<int:pk_1>/publish/', BlogViewSet.as_view({'put': 'publish_post'}), name='publish_post'),
    path('blogs/<int:pk>/unpublic_post/', BlogViewSet.as_view({'put': 'unpublic_post'}), name='unpublic_post'),
    path('blogs/sort_by_date/', BlogViewSet.as_view({'get': 'sort_blogs_by_date'}), name='sort_blogs_by_date'),
    path('blogs/create/', BlogViewSet.as_view({'post': 'create'}), name='create_blog'),
    path('blogs/<int:blog_id>/update/', BlogViewSet.as_view({'put': 'update'}), name='update'),
    # path('blogs/<int:pk>/delete/', BlogViewSet.as_view({'delete': 'destroy'}), name='delete_blog'),
    #http://localhost:8000/blogs/page/1?page=3
   #http://localhost:8000/blogs/page/1?page=1
    path('blogs/page/<int:pk>', BlogViewSet.as_view({'get':'page'}), name='page'),
    path('blogs/restore-blog/<int:id>', BlogViewSet.as_view({'put':'restore_blog'}), name='restore_blog'),
    path('blogs/delete-blog/<int:id>', BlogViewSet.as_view({'put':'delete_blog_temp'}), name='delete_blog_temp'),
    path('blogs/drop-blog/<int:id>', BlogViewSet.as_view({'delete':'destroy_blog'}), name='destroy_blog'),

    path('blogs/search/author/<str:author>/', BlogViewSet.as_view({'get': 'search_blog_by_author'})),
    path('blogs/search/title/<str:title>/', BlogViewSet.as_view({'get': 'search_blog_by_title'})),
    path('blogs/search/content/<str:content>/', BlogViewSet.as_view({'get': 'search_blog_by_content'})),
    path('blogs/delete_log/<int:pk>', BlogViewSet.as_view({'get': 'get_deleted_log_by_post'})),
    path('blogs/update_log/<int:pk>', BlogViewSet.as_view({'get': 'get_updated_log_by_post'})),
    path('blogs/updates/<int:blog_id>/', BlogViewSet.as_view({'put': 'update'}), name='blog-update'),
    ]
 



