from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from utils.paginate import paginate_queryset
from users.mixins import RequestUserOnlyMixin, GetRequestUseIdrMixin
from users.models import Profile
from .forms import EventCreateForm, CommentCreateForm
from .models import Event, EventComment, EventCommentMessage

from group.models import Group
from blogs.mixins import RequestUserIsAdministrator
from events.mixins import (EventCommentPkRequestUserIsAdministrator,
                           GroupPkRequestUserIsAdministrator,
                           RequestUserIsInTheEvent,
                           EventPkRequestUserIsAdministrator,
                           GroupGroup_PkRequestUserIsAdministrator
                           )

from users.mixins import get_user_id, GetRequestUseIdrMixin
from message.models import EventJoinedMessage



# class BlogCreate(RequestUserIsAdministrator, LoginRequiredMixin,  generic.CreateView):
#     model = Blog
#     template_name = 'blogs/post_create.html'
#     form_class = PostCreateForm
#
#     def get(self, request, *args, **kwargs):
#         print('hello')
#         print(self.kwargs['pk'])
#         return super().get(self, request, *args, **kwargs)
#
#
#     def form_valid(self, form):
#         pk = self.kwargs['pk']

@login_required
def create_event(request, group_pk, **kwargs):
    context = get_user_id(request, **kwargs)

    form = EventCreateForm(request.POST or None, request.FILES or None)
    context['form']= form
    template_name = 'events/event_create.html'

    if request.method == 'POST' and form.is_valid():
        related_group = get_object_or_404(Group, pk=group_pk)
        print(related_group)
        blog = form.save(commit=False)
        # print(blogs.posted_group)
        blog.posted_group = related_group
        form.save()
        return redirect('group:group_list')

    return render(request, template_name, context)

def event_detail(request, event_pk, **kwargs):
    context = get_user_id(request, **kwargs)
    template_name = 'events/event_detail.html'

    event = get_object_or_404(Event, pk=event_pk)
    context['event'] = event

    comments = EventComment.objects.filter(event=event)
    context['comments'] = comments
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid() and request.user.is_authenticated:
        posted_comment = form.save(commit=False)
        user_profile = get_object_or_404(Profile, user=request.user)
        posted_comment.user = user_profile
        posted_comment.event = event
        form.save()
        form = CommentCreateForm()

        post_group_administrators = event.posted_group.administrator.all()
        for post_group_administrator in post_group_administrators:
            EventCommentMessage.objects.create(administrator=post_group_administrator, comment=posted_comment)
        return redirect(reverse('events:event_detail', kwargs={'event_pk':event.pk}))

    context['form'] = form
    return render(request, template_name, context)



class EventUpdate(GetRequestUseIdrMixin, EventPkRequestUserIsAdministrator, LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'events/event_update.html'

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'event_pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            event = get_object_or_404(Event, pk=self.kwargs['pk'])
            prefecture_list = []
            for prefecture in event.prefecture.all():
                prefecture_list.append(int(prefecture.prefecture))
            print(prefecture_list)

            context['prefecture_list'] = prefecture_list
        elif self.request.method == 'POST':
            event = get_object_or_404(Event, pk=self.kwargs['pk'])
            prefecture_list = []
            prefectures = self.request.POST.getlist('prefecture')
            for prefecture in prefectures:
                prefecture_list.append(int(prefecture))
            print(prefecture_list)

            context['prefecture_list'] = prefecture_list

        return context




def event_list(request, group_pk, **kwargs):
    context = get_user_id(request, **kwargs)
    group = get_object_or_404(Group, pk=group_pk)
    context['group'] = group
    events = Event.objects.filter(posted_group=group).order_by('-event_day')
    page_obj = paginate_queryset(request, events, 15)
    # page = request.GET.getlist('page')

    # print(page_obj.number) 現在のページ番号を返す

    context['events'] = page_obj.object_list
    context['page_obj'] = page_obj

    # context['events'] = events
    template_name = 'events/event_list.html'
    if request.user.is_authenticated:
        user_profile =get_object_or_404(Profile, user=request.user)
        is_administrator = user_profile in group.administrator.all()
        context['is_administrator'] = is_administrator
    return render(request, template_name, context)


class EventDelete(LoginRequiredMixin, EventPkRequestUserIsAdministrator, GetRequestUseIdrMixin,generic.DeleteView):
    model = Event
    template_name = 'events/event_delete.html'


    def get_success_url(self):
        group = get_object_or_404(Event, pk=self.kwargs['pk']).posted_group
        return reverse_lazy('events:event_list', kwargs={'group_pk': group.pk})




class AllEventCommentList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'events/all_event_comment.html'
    context_object_name = 'event_comments'
    paginate_by = 10


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        groups = Group.objects.filter(administrator=user_profile)




        event_comment_filter = Q()
        # print(post_comment_filter)
        print('-'*20)
        for group in groups:
            for event in group.event_set.all():
                for each_comment in event.eventcomment_set.all():
                    print(each_comment)
                    event_comment_filter |= Q(comment=each_comment)

        event_comments = EventComment.objects.filter(event_comment_filter).order_by('-commented_at')
        return event_comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_profile = get_object_or_404(Profile, user=self.request.user)
        # group = get_object_or_404(Group, user=user_profile)
        # context['group'] = group
        return context

class EventCommentList(GetRequestUseIdrMixin, EventPkRequestUserIsAdministrator, generic.ListView):
    template_name = 'events/event_comment.html'
    context_object_name = 'event_comments'
    paginate_by = 10


    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        event_comments = EventComment.objects.filter(event=event).order_by('-commented_at')
        return event_comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Event, pk=self.kwargs['event_pk']).posted_group
        context['group'] = group
        return context


class EventCommentDetail(LoginRequiredMixin, GetRequestUseIdrMixin, EventCommentPkRequestUserIsAdministrator, generic.DetailView):
    model = EventComment
    template_name = 'events/event_comment_detail.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, user=request.user)

        comment = get_object_or_404(EventComment, pk=self.kwargs['eventcomment_pk'])
        comment_message = comment.eventcommentmessage_set.filter(administrator=user)
        try:
            comment_message = comment.eventcommentmessage_set.get(administrator=user)
        except EventCommentMessage.DoesNotExist:
            return super().get(request, *args, **kwargs)

        try:
            comment_message.has_read = True
            comment_message.save()
            return super().get(request, *args, **kwargs)
        except UnboundLocalError:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(EventComment, pk=self.kwargs['eventcomment_pk']).event.posted_group
        context['group'] = group
        return context



@login_required
def join_event(request, event_pk, **kwargs):
    context = get_user_id(request, **kwargs)
    join_event = get_object_or_404(Event, pk=event_pk)
    context['join_event'] = join_event

    if request.method == 'GET':
        template_name = 'events/event_join.html'
        return render(request, template_name, context)


    if request.method == 'POST':
        request_user = get_object_or_404(Profile, user=request.user)

        if request_user in join_event.joinned_user.all():
            template_name = 'events/already_joinned_event.html'
            return render(request, template_name, context)

        # if request_user in join_event.applied_user.all():
        #     template_name = 'group/event_join_already_appied.html'
        #     return render(request, template_name, context)


        group_administrators = join_event.posted_group.administrator.all()

        join_event.joinned_user.add(request_user)

        for group_administrator in group_administrators:
            EventJoinedMessage.objects.create(administrator=group_administrator, applied_user=request_user, event=join_event)

        template_name = 'events/event_join_apply_done.html'

        return render(request, template_name, context)

class CancelEvent(LoginRequiredMixin, RequestUserIsInTheEvent, GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'events/cancel_event.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        context['event'] = event
        context['user'] = user_profile

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = get_object_or_404(Profile, user=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        context['event'] = event
        context['user'] = user_profile

        try:
            if self.request.POST['delete_complete'] == 'delete_complete':
                event.joinned_user.remove(user_profile)
                return redirect('events:cancel_event_done')

        except KeyError:
            return redirect('group:group_list')


class CancelEventDone(LoginRequiredMixin,GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'events/cancel_event_done.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().get(request, *args, **kwargs)




# class DeleteEvent(LoginRequiredMixin, EventEvent_PkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.TemplateView):
#     template_name = 'events/delete_event.html'
#
#     def get(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = get_object_or_404(Profile, user=self.request.user)
#         event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
#         context['event'] = event
#         context['user'] = user_profile
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         user_profile = get_object_or_404(Profile, user=self.request.user)
#         event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
#         context['event'] = event
#         context['user'] = user_profile
#         try:
#             if self.request.POST['delete_complete'] == 'delete_complete':
#                 event.delete()
#                 return redirect('events:delete_event_done')
#             return redirect('group:group_list')
#
#         except KeyError:
#             return redirect('group:group_list')
#
#
# class DeleteEventDone(LoginRequiredMixin,GetRequestUseIdrMixin, generic.TemplateView):
#     template_name = 'events/delete_event_done.html'
#
#     def get(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return super().get(request, *args, **kwargs)
#

class EventJoinList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'events/event_join_list.html'
    context_object_name = 'events'
    paginate_by = 10


    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)

        events = Event.objects.filter(joinned_user=user_profile)
        print(events)

        return events

class RecentEventList(GetRequestUseIdrMixin, generic.ListView):
    template_name = 'events/recent_event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):

        events = Event.objects.filter(event_day__gte=timezone.now()).order_by('-event_day')

        return events