from django.urls import path
from . import views


app_name= 'events'

urlpatterns = [
    # groupのpkです
    path('event_create/<int:group_pk>/', views.create_event, name='create_event'),
    # eventのpkです
    path('event_detail/<int:event_pk>/', views.event_detail, name='event_detail'),
    path('event_update/<int:pk>/', views.EventUpdate.as_view(), name='update_event'),
    path('event_delete/<int:pk>/', views.EventDelete.as_view(), name='delete_event'),
    # groupのpkです
    path('event_list/<int:group_pk>/', views.event_list, name='event_list'),
    path('event_join_list/', views.EventJoinList.as_view(), name='event_join_list'),
    path('recent_event_list/', views.RecentEventList.as_view(), name='recent_event_list'),
    path('all_comment_list/', views.AllEventCommentList.as_view(), name='all_comment_list'),

    path('comment_list/<int:event_pk>/', views.EventCommentList.as_view(), name='comment_list'),
    # コメントのpkです
    path('comment/<int:eventcomment_pk>/', views.EventCommentDetail.as_view(), name='comment_detail'),
    # eventのpk
    path('event_join/<int:event_pk>/', views.join_event, name='event_join'),

    path('event_cancel/<int:event_pk>/', views.CancelEvent.as_view(), name='cancel_event'),
    path('event_cancel_done/', views.CancelEventDone.as_view(), name='cancel_event_done'),
    # path('delete_event/<int:event_pk>', views.DeleteEvent.as_view(), name='delete_event'),
    # path('delete_event_done/', views.DeleteEventDone.as_view(), name='delete_event_done'),

]
