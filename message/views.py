from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q



from users.models import Profile
from users.mixins import get_user_id, GetRequestUseIdrMixin
from group.mixins import RequestUserIsInTheGroup, GroupPkRequestUserIsAdministrator
from events.models import Event, EventCommentMessage
from events.mixins import EventPkRequestUserIsAdministrator
from group.models import Group
from blogs.models import BlogCommentMessage, Blog
from blogs.mixins import PostPkRequestUserIsAdministrator
from .forms import InnerGroupMessageCreateForm, EventMessageCreateForm
from .models import (
                     GroupApplyMessage,
                     InnerGroupMessage,
                     HasReadInnerGroupMessage,
                     EventMessage,
                     HasReadEventMessage,
                     AdminMessage,
                     EventJoinedMessage,
                     ApplyAdministratorMessage,
                     )


class InnerGroupMessageCreate(LoginRequiredMixin, GroupPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.CreateView):
    model = InnerGroupMessage
    form_class = InnerGroupMessageCreateForm
    template_name = 'message/inner_group_message_create.html'
    success_url = reverse_lazy('group:group_list')


    def form_valid(self, form):
        related_group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        message = form.save(commit=False)

        message.group = related_group
        message.save()

        group_members = related_group.member.all()
        for group_member in group_members:
            HasReadInnerGroupMessage.objects.create(group_message=message, user=group_member)

        return super().form_valid(form)


class InnerGroupMessageList(LoginRequiredMixin, RequestUserIsInTheGroup, GetRequestUseIdrMixin,  generic.ListView):
    template_name = 'message/inner_group_message_list.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        messages = InnerGroupMessage.objects.filter(group=group).order_by('-sent_at')
        return messages


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


# class InnerGroupMessageList(LoginRequiredMixin, RequestUserIsInTheGroup, GetRequestUseIdrMixin, generic.ListView):
#     template_name = 'message/inner_group_message_list.html'
#     context_object_name = 'messages'
#
#     def get_queryset(self):
#         user_profile =get_object_or_404(Profile, user=self.request.user)
#         InnerGroupMessage.objects.filter()
#         belonging_groups = Group.objecst.filter(member=user_profile)
#         messages = group.sender.all().order_by('-sent_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class EventMessageCreate(LoginRequiredMixin, EventPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.CreateView):
    model = EventMessage
    form_class = EventMessageCreateForm
    template_name = 'message/event_message_create.html'
    success_url = reverse_lazy('group:group_list')


    def form_valid(self, form):
        related_event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        sent_administrator = get_object_or_404(Profile, user=self.request.user)
        message = form.save(commit=False)

        message.event = related_event
        message.administrator = sent_administrator
        message.save()

        event_joiners = related_event.joinned_user.all()
        for event_joiner in event_joiners:
            HasReadEventMessage.objects.create(event_message=message, user=event_joiner)

        return super().form_valid(form)


@login_required
def message_list(request,  *args, **kwargs):
    context = get_user_id(request, **kwargs)
    template_name= 'message/message_list.html'
    user_profile = get_object_or_404(Profile, user=request.user)


    admin_messages = list(AdminMessage.objects.filter(user=user_profile).values())
    apply_administrator_messsages = list(ApplyAdministratorMessage.objects.filter(user=user_profile).values())
    admin_messages.extend(apply_administrator_messsages)

    admin_messages.sort(key=lambda item:item['sent_at'], reverse=True)
    admin_message_list = []
    admin_messages_count = 0
    for admin_message in admin_messages:
        try:
            each_admin_message =  AdminMessage.objects.get(**admin_message)
            admin_message_list.append(each_admin_message)

        except:
            each_admin_message = ApplyAdministratorMessage.objects.get(**admin_message)
            admin_message_list.append(each_admin_message)

        if each_admin_message.has_read == False:
            admin_messages_count += 1


    context['admin_messages'] = admin_message_list[:5]
    context['admin_messages_count'] = admin_messages_count


    has_read_event_messages = HasReadEventMessage.objects.filter(user=user_profile).order_by('-pk')
    has_read_event_messages_count = has_read_event_messages.filter(has_read=False).count()
    has_read_event_messages = has_read_event_messages[:5]
    context['has_read_event_messages'] = has_read_event_messages
    context['has_read_event_messages_count'] = has_read_event_messages_count


    has_read_inner_group_messages = HasReadInnerGroupMessage.objects.filter(user=user_profile).order_by('-pk')
    has_read_inner_group_messages_count = has_read_inner_group_messages.filter(has_read=False).count()
    has_read_inner_group_messages = has_read_inner_group_messages[:5]
    context['has_read_inner_group_messages'] = has_read_inner_group_messages
    context['has_read_inner_group_messages_count'] = has_read_inner_group_messages_count


    event_join_messages = EventJoinedMessage.objects.filter(administrator=user_profile).order_by('-pk')
    event_join_messages_count = event_join_messages.filter(has_read=False).count()
    event_join_messages = event_join_messages[:5]
    context['event_join_messages'] = event_join_messages
    context['event_join_messages_count'] = event_join_messages_count


    group_apply_messsages = GroupApplyMessage.objects.filter(administrator=user_profile).order_by('-pk')
    group_apply_messsages_count = group_apply_messsages.filter(has_read=False).count()
    group_apply_messsages = group_apply_messsages[:5]
    context['group_apply_messages'] = group_apply_messsages
    context['group_apply_messages_count'] = group_apply_messsages_count


    event_comment_messages = EventCommentMessage.objects.filter(administrator=user_profile).order_by('-pk')
    event_comment_messages_count = event_comment_messages.filter(has_read=False).count()
    event_comment_messages = event_comment_messages[:5]
    context['event_comment_messages'] = event_comment_messages
    context['event_comment_messages_count'] = event_comment_messages_count


    post_comment_messages = BlogCommentMessage.objects.filter(administrator=user_profile).order_by('-pk')
    post_comment_messages_count = post_comment_messages.filter(has_read=False).count()
    post_comment_messages = post_comment_messages[:5]
    context['post_comment_messages'] = post_comment_messages
    context['post_comment_messages_count'] = post_comment_messages_count


    is_administrator = Group.objects.filter(administrator=user_profile).exists()
    context['is_administrator'] = is_administrator

    return render(request, template_name, context)


class EventMessageList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'message/event_message_list.html'
    context_object_name = 'has_read_event_messages'
    paginate_by = 20


    def get_queryset(self):

        user_profile = get_object_or_404(Profile, user=self.request.user)
        has_read_event_messages = HasReadEventMessage.objects.filter(user=user_profile).order_by('-pk')
        # print(has_read_event_messages.event_message)
        return has_read_event_messages



class EventMessageListForHost(LoginRequiredMixin, EventPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'message/event_message_list_for_host.html'
    context_object_name = 'event_messages'
    paginate_by = 20


    def get_queryset(self):
        event_messages = get_object_or_404(Event, pk=self.kwargs['event_pk']).eventmessage_set.all().order_by('-pk')
        return event_messages
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event= get_object_or_404(Event, pk=self.kwargs['event_pk'])
        context['event'] = event
        return context



class EachEventMessageList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'message/each_event_message_list.html'
    context_object_name = 'has_read_event_messages'
    paginate_by = 20


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        has_read_event_messages = HasReadEventMessage.objects.filter(user=user_profile, event_message__event=event).order_by('-pk')
        return has_read_event_messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        context['event'] = event
        group = event.posted_group
        context['group'] = group
        return context






class AdminMessageList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'message/admin_message_list.html'
    context_object_name = 'admin_messages'
    paginate_by = 20



    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)


        admin_messages = list(AdminMessage.objects.filter(user=user_profile).values())
        apply_administrator_messsages = list(ApplyAdministratorMessage.objects.filter(user=user_profile).values())

        admin_messages.extend(apply_administrator_messsages)

        admin_messages.sort(key=lambda item: item['sent_at'], reverse=True)
        admin_message_list = []

        for admin_message in admin_messages:
            try:
                each_admin_message = AdminMessage.objects.get(**admin_message)
                admin_message_list.append(each_admin_message)
            except:
                each_admin_message = ApplyAdministratorMessage.objects.get(**admin_message)
                admin_message_list.append(each_admin_message)


        return admin_message_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_profile = get_object_or_404(Profile, user=self.request.user)
    #
    #     AdminMessage.objects.filter(user=user_profile) in


class EachEventJoinMessageList(LoginRequiredMixin, EventPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.ListView):
    """イベントに参加しました！という通知一覧"""
    template_name = 'message/event_joined_message_list.html'
    context_object_name = 'event_join_messages'
    paginate_by = 20


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        event_join_messages = EventJoinedMessage.objects.filter(administrator=user_profile, event=event).order_by('-pk')
        return event_join_messages


class EachGroupApplyMessageList(LoginRequiredMixin, GroupPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.ListView):
    """ グループに加入しましたというメッセージ一覧"""
    template_name = 'message/group_apply_message_list.html'
    context_object_name = 'group_apply_messages'
    paginate_by = 20


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        group_apply_messages = GroupApplyMessage.objects.filter(administrator=user_profile, group=group).order_by('-pk')

        return group_apply_messages


class EachEventCommentMessageList(LoginRequiredMixin, EventPkRequestUserIsAdministrator, GetRequestUseIdrMixin,
                               generic.ListView):
    """各イベントのコメント一覧を表示　既読をつけるため"""
    template_name = 'message/event_comment_message_list.html'
    context_object_name = 'event_comment_messages'
    paginate_by = 20


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, pk=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        event_comment_messages = EventCommentMessage.objects.filter(administrator=user_profile, comment__event=event).order_by('-pk')
        return event_comment_messages


class EachPostCommentMessageList(LoginRequiredMixin, PostPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.ListView):
    """各ブログの投稿のコメント一覧を表示 既読をつけるため"""
    template_name = 'message/post_comment_message_list.html'
    context_object_name = 'post_comment_messages'
    paginate_by = 20

    def get_queryset(self):
        user_profile = get_object_or_404(Profile, pk=self.request.user)
        post = get_object_or_404(Blog, pk=self.kwargs['post_pk'])
        post_comment_messages = BlogCommentMessage.objects.filter(administrator=user_profile, comment__post=post).order_by('-pk')
        return post_comment_messages

