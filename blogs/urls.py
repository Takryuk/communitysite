from django.urls import path
from . import views


app_name = 'blogs'

urlpatterns = [
    # groupのpkです
    path('post_create/<int:group_pk>/', views.create_post, name='create_post'),
    # blogのpkです
    path('post_detail/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('post_update/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),
    path('post_delete/<int:pk>/', views.PostDelete.as_view(), name='delete_post'),
    # groupのpkです
    path('post_list/<int:group_pk>/', views.PostList.as_view(), name='post_list'),
    path('recent_post_list/', views.RecentPostList.as_view(), name='recent_post_list'),

    path('comment_list/<int:group_pk>/', views.BlogCommentList.as_view(), name='comment_list'),
    # コメントのpkです
    path('comment/<int:postcomment_pk>/', views.BlogCommentDetail.as_view(), name='comment_detail'),
    # path('delete_post/<int:post_pk>', views.DeletePost.as_view(), name='delete_post'),
    # path('delete_post_done/', views.DeletePostDone.as_view(), name='delete_post_done'),

]
