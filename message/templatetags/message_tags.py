from django.shortcuts import render, redirect, reverse, get_object_or_404
from django import template


from users.models import Profile
from blogs.models import BlogCommentMessage
from events.models import EventCommentMessage
from group.models import Group
from message.models import (
                     GroupApplyMessage,
                     InnerGroupMessage,
                     HasReadInnerGroupMessage,
                     EventMessage,
                     HasReadEventMessage,
                     AdminMessage,
                     EventJoinedMessage,
                     ApplyAdministratorMessage,
                     )


register = template.Library()


@register.simple_tag
def has_read_admin_message(admin_message):
    if admin_message.has_read:
        return ''

    else:
        admin_message.has_read = True
        admin_message.save()
        return '<small>未読</small>   '


@register.simple_tag
def has_read_inner_group_message(request, message):
    user = get_object_or_404(Profile, user=request.user)
    try:
        group_message = message.hasreadinnergroupmessage_set.get(user=user)
    except HasReadInnerGroupMessage.DoesNotExist:
        return ''
    try:
        if group_message.has_read:
            return ''
        else:
            group_message.has_read = True
            group_message.save()
            return '<small>未読</small>   '
    except UnboundLocalError:
        pass


@register.simple_tag
def has_read_event_message(has_read_event_message):
    if has_read_event_message.has_read:
        return ''

    else:
        has_read_event_message.has_read = True
        has_read_event_message.save()
        return '<small>未読</small>   '


@register.simple_tag
def has_read_event_join_message(event_join_message):
    if event_join_message.has_read:
        return ''

    else:
        event_join_message.has_read = True
        event_join_message.save()
        return '<small>未読</small>   '


@register.simple_tag
def has_read_group_apply_message(group_apply_message):
    if group_apply_message.has_read:
        return ''

    else:
        group_apply_message.has_read = True
        group_apply_message.save()
        return '<small>未読</small>   '


@register.simple_tag
def has_read_event_comment_message(event_comment_message):
    if event_comment_message.has_read:
        return ''

    else:
        event_comment_message.has_read = True
        event_comment_message.save()
        return '<small>未読</small>   '


@register.simple_tag
def has_read_post_comment_message(post_comment_message):
    if post_comment_message.has_read:
        return ''

    else:
        post_comment_message.has_read = True
        post_comment_message.save()
        return '<small>未読</small>   '



# @register.simple_tag
# def is_before_administrator(request, admin_message):
#     user = get_object_or_404(Profile, user=request.user)
#
#     if user in admin_message.group.before_administrator.all():
#         return '<p><a href="{% url \'group:admit_being_administrator\' user_pk=admin_message.user.pk group_pk=admin_message.group.pk %}" >管理者要請を承諾</a></p>'
#     else:
#         return ''


@register.inclusion_tag('inclusion_tag/admin_tag.html', takes_context=True)
def is_before_administrator(context):
    user = get_object_or_404(Profile, user=context['request'].user)
    admin_message = context['admin_message']
    is_in_before_administrator = user in admin_message.group.before_administrator.all()

    if is_in_before_administrator:
        return {'user':user, 'admin_message': admin_message, 'is_in_administrator': is_in_before_administrator}



@register.simple_tag
def count_new_message(request):
    try:
        user_profile = get_object_or_404(Profile, user=request.user)


        new_message_counter = 0
        new_message_counter += AdminMessage.objects.filter(user=user_profile, has_read=False).count()
        new_message_counter += ApplyAdministratorMessage.objects.filter(user=user_profile, has_read=False).count()
        new_message_counter += HasReadEventMessage.objects.filter(user=user_profile, has_read=False).count()
        new_message_counter += HasReadInnerGroupMessage.objects.filter(user=user_profile, has_read=False).count()
        new_message_counter += EventJoinedMessage.objects.filter(administrator=user_profile, has_read=False).count()
        new_message_counter += GroupApplyMessage.objects.filter(administrator=user_profile, has_read=False).count()
        new_message_counter += EventCommentMessage.objects.filter(administrator=user_profile, has_read=False).count()
        new_message_counter +=  BlogCommentMessage.objects.filter(administrator=user_profile, has_read=False).count()

        if new_message_counter:
            return str(new_message_counter) + '件'
        else:
            return ''
    except:
        return ''
    # admin_messages = list(AdminMessage.objects.filter(user=user_profile, has_read=False).values())
    # apply_administrator_messsages = list(ApplyAdministratorMessage.objects.filter(user=user_profile, has_read=False).values())
    # admin_messages.extend(apply_administrator_messsages)
    #
    # admin_messages.sort(key=lambda item: item['sent_at'], reverse=True)
    # admin_message_list = []
    # for admin_message in admin_messages:
    #     try:
    #         each_admin_message = AdminMessage.objects.get(**admin_message)
    #         admin_message_list.append(each_admin_message)
    #     except:
    #         each_admin_message = ApplyAdministratorMessage.objects.get(**admin_message)
    #         admin_message_list.append(each_admin_message)
    #
    # context['admin_messages'] = admin_message_list[:5]

    # has_read_event_messages = HasReadEventMessage.objects.filter(user=user_profile).order_by('-pk')[:5]
    # context['has_read_event_messages'] = has_read_event_messages
    #
    # has_read_inner_group_messages = HasReadInnerGroupMessage.objects.filter(user=user_profile).order_by('-pk')[:5]
    # context['has_read_inner_group_messages'] = has_read_inner_group_messages
    #
    # event_join_messages = EventJoinedMessage.objects.filter(administrator=user_profile).order_by('-pk')[:5]
    # context['event_join_messages'] = event_join_messages
    #
    # group_apply_messsages = GroupApplyMessage.objects.filter(administrator=user_profile).order_by('-pk')[:5]
    # context['group_apply_messages'] = group_apply_messsages
    #
    # event_comment_messages = EventCommentMessage.objects.filter(administrator=user_profile).order_by('-pk')[:5]
    # context['event_comment_messages'] = event_comment_messages
    #
    # post_comment_messages = BlogCommentMessage.objects.filter(administrator=user_profile).order_by('-pk')[:5]
    # context['post_comment_messages'] = post_comment_messages
    #
    # is_administrator = Group.objects.filter(administrator=user_profile).exists()
    # context['is_administrator'] = is_administrator