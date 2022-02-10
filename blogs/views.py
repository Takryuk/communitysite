from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone


from users.mixins import RequestUserOnlyMixin, GetRequestUseIdrMixin

from users.models import Profile

from .forms import PostCreateForm, CommentCreateForm

from group.models import Group
from group.mixins import GroupPkRequestUserIsAdministrator, RequestUserIsAdministrator
from .models import Blog, BlogComment, BlogCommentMessage
from .mixins import (
    PostCommentPkRequestUserIsAdministrator,
    PostPkRequestUserIsAdministrator,
)

from users.mixins import get_user_id, GetRequestUseIdrMixin


@login_required
def create_post(request, group_pk, **kwargs):
    context = get_user_id(request, **kwargs)

    form = PostCreateForm(request.POST or None, request.FILES or None)
    context['form']= form
    template_name = 'blogs/post_create.html'

    if request.method == 'POST' and form.is_valid():
        related_group = get_object_or_404(Group, pk=group_pk)
        blog = form.save(commit=False)
        blog.posted_group = related_group
        form.save()
        return redirect('group:group_list')

    return render(request, template_name, context)



def post_detail(request, post_pk, **kwargs):
    context = get_user_id(request, **kwargs)
    template_name = 'blogs/post_detail.html'

    post = get_object_or_404(Blog, pk=post_pk)
    context['post'] = post

    comments = BlogComment.objects.filter(post=post)
    context['comments'] = comments
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid() and request.user.is_authenticated:
        posted_comment = form.save(commit=False)
        user_profile = get_object_or_404(Profile, user=request.user)
        posted_comment.user = user_profile
        posted_comment.post = post
        form.save()
        form = CommentCreateForm()
        post_group_administrators = post.posted_group.administrator.all()
        for post_group_administrator in post_group_administrators:
            BlogCommentMessage.objects.create(administrator=post_group_administrator, comment=posted_comment)

        return redirect(reverse('blogs:post_detail', kwargs={'post_pk':post.pk}))
    context['form'] = form

    return render(request, template_name, context)



class PostUpdate(GetRequestUseIdrMixin, PostPkRequestUserIsAdministrator, LoginRequiredMixin, generic.UpdateView):
    model = Blog
    form_class = PostCreateForm
    template_name = 'blogs/post_update.html'

    def get_success_url(self):
        return reverse_lazy('blogs:post_detail', kwargs={'post_pk':self.kwargs['pk']})


class PostList(GetRequestUseIdrMixin, generic.ListView):
    context_object_name = 'posts'
    template_name = 'blogs/post_list.html'
    paginate_by = 15
    def get_queryset(self, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        posts = Blog.objects.filter(posted_group=group).order_by('-posted_at')
        return posts

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        if self.request.user.is_authenticated:
            user_profile = get_object_or_404(Profile, user=self.request.user)
            is_administrator = user_profile in group.administrator.all()
            context['is_administrator'] = is_administrator
        return context




class PostDelete(LoginRequiredMixin, PostPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.DeleteView):
    model = Blog
    template_name = 'blogs/post_delete.html'
    def get_success_url(self):
        group = get_object_or_404(Blog, pk=self.kwargs['pk']).posted_group
        return reverse_lazy('blogs:post_list', kwargs={'group_pk': group.pk})


class BlogCommentList(GetRequestUseIdrMixin, GroupPkRequestUserIsAdministrator, generic.ListView):
    template_name = 'blogs/post_comment.html'
    context_object_name = 'post_comments'


    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        all_posts = group.blog_set.all()

        post_comment_filter = Q()

        for post in all_posts:
            for each_comment in post.blogcomment_set.all():
                print(each_comment)
                post_comment_filter |= Q(comment=each_comment)

        post_comments = BlogComment.objects.filter(post_comment_filter).order_by('-commented_at')
        print(post_comments)
        return post_comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class BlogCommentList(GetRequestUseIdrMixin, GroupPkRequestUserIsAdministrator, generic.ListView):
    template_name = 'blogs/post_comment.html'
    context_object_name = 'post_comments'
    paginate_by = 10


    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        all_posts = group.blog_set.all()

        post_comment_filter = Q()

        for post in all_posts:
            for each_comment in post.blogcomment_set.all():
                print(each_comment)
                post_comment_filter |= Q(comment=each_comment)

        post_comments = BlogComment.objects.filter(post_comment_filter).order_by('-commented_at')
        print(post_comments)
        return post_comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class BlogCommentDetail(GetRequestUseIdrMixin, PostCommentPkRequestUserIsAdministrator, generic.DetailView):
    model = BlogComment
    template_name = 'blogs/post_comment_detail.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, user=request.user)
        comment = get_object_or_404(BlogComment, pk=self.kwargs['postcomment_pk'])
        try:
            comment_message = comment.blogcommentmessage_set.get(administrator=user)
        except BlogCommentMessage.DoesNotExist:
            return super().get(request, *args, **kwargs)

        try:
            comment_message.has_read = True
            comment_message.save()
            return super().get(request, *args, **kwargs)
        except UnboundLocalError:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['postcomment_pk'])
        context['group'] = group
        return context


class RecentPostList(GetRequestUseIdrMixin, generic.ListView):
    template_name = 'blogs/recent_post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):

        posts = Blog.objects.order_by('-posted_at')

        return posts


# class DeletePost(LoginRequiredMixin, PostPost_PkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.TemplateView):
#     template_name = 'blogs/delete_post.html'
#
#     def get(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = get_object_or_404(Profile, user=self.request.user)
#         post = get_object_or_404(Blog, pk=self.kwargs['post_pk'])
#         context['post'] = post
#         context['user'] = user_profile
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         user_profile = get_object_or_404(Profile, user=self.request.user)
#         post = get_object_or_404(Blog, pk=self.kwargs['post_pk'])
#         context['post'] = post
#         context['user'] = user_profile
#         try:
#             if self.request.POST['delete_complete'] == 'delete_complete':
#                 post.delete()
#                 return redirect('blogs:delete_post_done')
#             return redirect('group:group_list')
#
#         except KeyError:
#             return redirect('group:group_list')
#
#
# class DeletePostDone(LoginRequiredMixin,PostPost_PkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.TemplateView):
#     template_name = 'blogs/delete_post_done.html'
#
#     def get(self, request, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return super().get(request, *args, **kwargs)
#
#
#
