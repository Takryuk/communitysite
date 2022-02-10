from django.contrib import admin
from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    # グループのpk
    path('inner_group_message_create/<int:group_pk>', views.InnerGroupMessageCreate.as_view(), name='create_inner_group_message'),
    path('inner_group_message_list/<int:group_pk>.', views.InnerGroupMessageList.as_view(), name='inner_group_message_list'),

    # eventのpk
    path('event_message_create/<int:event_pk>/', views.EventMessageCreate.as_view(), name='create_event_message'),

    # userのpk
    path('message_list/', views.message_list, name='message_list'),
    path('each_event_message_list/<int:event_pk>/', views.EachEventMessageList.as_view(), name='each_event_message_list'),
    path('event_message_list/', views.EventMessageList.as_view(), name='event_message_list'),
    path('event_message_list_for_host/<int:event_pk>', views.EventMessageListForHost.as_view(), name='event_message_list_for_host'),
    path('event_join_message_list/<int:event_pk>/', views.EachEventJoinMessageList.as_view(), name='event_join_message_list'),
    path('group_apply_message_list/<int:group_pk>/', views.EachGroupApplyMessageList.as_view(), name='group_apply_message_list'),
    path('event_comment_message_list/<int:event_pk>/', views.EachEventCommentMessageList.as_view(), name='event_comment_message_list'),
    path('post_comment_message_list/<int:post_pk>/', views.EachPostCommentMessageList.as_view(),name='post_comment_message_list'),

    # userのpk
    path('admin_message_list/', views.AdminMessageList.as_view(), name='admin_message_list'),


    # path('group_create_done/', views.GroupCreateDone.as_view(), name='group_create_done'),
    # path('group_detail/<int:pk>', views.group_detail, name='group_detail'),
    # path('group_join/<int:pk>', views.join_group, name='group_join'),
    # path('group_not_display/', views.GroupNotDisplay.as_view(), name='group_not_display'),
    # # path('group_list/', views.GroupList.as_view(), name='group_list'),
    # path('group_list/', views.post_index, name='group_list'),
    # path('<int:group_pk>/approve_user/<int:user_pk>/', views.approve_applied_user, name='approve_user'),


]
