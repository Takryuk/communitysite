from django.contrib import admin
from django.urls import path

from . import views

app_name = 'group'

urlpatterns = [
    path('before_create/', views.BeforeCreate.as_view(), name='before_create'),
    path('group_create/', views.create_group, name='create_group'),
    # path('group_create/', views.CreateGroup.as_view(), name='create_group'),
    path('group_create_done/', views.GroupCreateDone.as_view(), name='group_create_done'),
    path('group_detail/<int:group_pk>', views.group_detail, name='group_detail'),

    # groupのpk
    path('group_update/<int:group_pk>', views.update_group, name='update_group'),
    path('group_join/<int:group_pk>', views.join_group, name='group_join'),
    path('group_not_display/', views.GroupNotDisplay.as_view(), name='group_not_display'),
    path('group_list/', views.group_list, name='group_list'),
    path('<int:group_pk>/approve_user/<int:user_pk>/', views.approve_applied_user, name='approve_user'),
    path('apply_administrator/<int:user_pk>/<int:group_pk>/', views.apply_administrator, name='apply_administrator'),
    path('admit_being_administrator/<int:user_pk>/<int:group_pk>/', views.admit_being_administrator, name='admit_being_administrator'),


    path('remove_user/<int:user_pk>/<int:group_pk>/', views.remove_user_from_group, name='remove_user'),
    path('group_member_list/<int:group_pk>/', views.GroupMemberList.as_view(), name='group_member_list'),
    path('group_member_list_for_all/<int:group_pk>/', views.GroupMemberListForAll.as_view(), name='group_member_list_for_all'),
    path('group_administrator_list_for_all/<int:group_pk>/', views.GroupAdministratorListForAll.as_view(), name='group_administrator_list_for_all'),
    path('leave_group/<int:group_pk>', views.LeaveGroup.as_view(), name='leave_group'),
    path('leave_group_done/', views.LeaveGroupDone.as_view(), name='leave_group_done'),
    path('delete_group/<int:group_pk>', views.DeleteGroup.as_view(), name='delete_group'),
    path('delete_group_done/', views.DeleteGroupDone.as_view(), name='delete_group_done'),
    path('managing_group/<int:group_pk>', views.ManageGroup.as_view(), name='managing_group'),
    path('belonging_group/', views.BelongingGroupList.as_view(), name='belonging_group'),
    path('belonging_group_info/<int:group_pk>', views.BelongingGroupInfo.as_view(), name='belonging_group_info'),
    path('group_info/<int:group_pk>', views.BelongingGroupInfo.as_view(), name='belonging_group_info'),
    path('stop_recruiting_member/<int:group_pk>', views.StopRecruitingMember.as_view(), name='stop_recruiting_member'),
]
