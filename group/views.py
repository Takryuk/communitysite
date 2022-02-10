from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.mixins import RequestUserOnlyMixin, GetRequestUseIdrMixin
from users.decorators import only_request_user_pk_user
from users.models import Profile
from users.mixins import get_user_id
from message.models import GroupApplyMessage, AdminMessage, ApplyAdministratorMessage
from .forms import (BeforeCreateConsentForm,
                    GroupCreateForm,
                    GroupSearchForm,
                    ApproveOrRefuseUserForm,
                    ApplyAdministratorForm,
                    AdmitOrRefuseBeingAdministratorForm,
                    RemoveUseForm,
                    )
from .models import GroupCategory, Group, GroupPrefecture
# Group
from .decorators import get_user_profile_id
from .mixins import RequestUserIsInTheGroup, GroupPkRequestUserIsAdministrator
from .decorators import group_pk_request_user_is_administrator



class BeforeCreate(LoginRequiredMixin, GetRequestUseIdrMixin, generic.FormView,):
    form_class = BeforeCreateConsentForm
    template_name = 'group/before_create.html'
    success_url = reverse_lazy('group:create_group')



class CreateGroup(LoginRequiredMixin, GetRequestUseIdrMixin, generic.CreateView):
    template_name = 'group/group_create.html'
    form_class = GroupCreateForm


    def get_success_url(self):
        return reverse_lazy('group:group_list')
        # return reverse_lazy('group:group_detail', kwargs={'group_pk':group_pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checked_category = self.request.POST.getlist('category')
        checked_prefecture = self.request.POST.getlist('prefecture')
        context['checked_category'] = checked_category
        context['checked_prefecture'] = checked_prefecture
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user = Profile.objects.get(user=self.request.user)
        group = form.save(commit=False)
        group.save()
        group.prefecture.set(form.cleaned_data['prefecture'])
        group.generation.set(form.cleaned_data['generation'])
        group.category.set(form.cleaned_data['category'])
        group.member.add(user)
        group.administrator.add(user)


        form.save_m2m()



        return redirect(reverse('group:group_detail', kwargs={'group_pk': group.pk}))



@login_required
def create_group(request):
    context = get_user_id(request)

    if request.method == 'GET':
        return redirect(reverse_lazy('group:before_create'))

    form = GroupCreateForm(request.POST or None, request.FILES or None)
    # print(context)
    # context = {}
    context['form'] = form

    id_category_number = 0
    category_outdoors = GroupCategory.objects.filter(category_sort='1')
    category_cultures = GroupCategory.objects.filter(category_sort='2')
    category_socials = GroupCategory.objects.filter(category_sort='3')

    print(request.POST.getlist('category'))

    checked_category =  request.POST.getlist('category')
    context['checked_category'] = checked_category
    checked_prefecture =  request.POST.getlist('prefecture')
    context['checked_prefecture'] = checked_prefecture
    print(checked_category)




    # category_outdoor_form = []
    # for category_outdoor in category_outdoors:
    #     if str(id_category_number+1) in checked_category:
    #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">'\
    #                            + '<input type="checkbox" name="category" value="' + str(id_category_number+1)\
    #                            +'" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked >'\
    #                            + category_outdoor.__str__() + '</label></li>')
    #         id_category_number += 1
    #     else:
    #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
    #                                      + '<input type="checkbox" name="category" value="' + str(
    #             id_category_number + 1) \
    #                                      + '" class ="form-horizontal" id="id_category_' + str(
    #             id_category_number) + '" >' \
    #                                      + category_outdoor.__str__() + '</label></li>')
    #         id_category_number += 1
    #
    #
    #
    # category_culture_form = []
    # for category_culture in category_cultures:
    #     if str(id_category_number+1) in checked_category:
    #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
    #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)\
    #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked>' \
    #                                  + category_culture.__str__() + '</label></li>')
    #         id_category_number += 1
    #     else:
    #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
    #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1) \
    #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '">' \
    #                                  + category_culture.__str__() + '</label></li>')
    #         id_category_number += 1
    #
    #
    # category_social_form = []
    # for category_social in category_socials:
    #     if str(id_category_number+1) in checked_category:
    #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
    #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)\
    #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked>' \
    #                                  + category_social.__str__() + '</label></li>')
    #         id_category_number += 1
    #     else:
    #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
    #                                     + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)
    #                                     + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" >' \
    #                                     + category_social.__str__() + '</label></li>')
    #         id_category_number += 1
    #
    # context['category_outdoor_form'] = category_outdoor_form
    # context['category_culture_form'] = category_culture_form
    # context['category_social_form'] = category_social_form





    # print(form.fields['category'])
    # print(form.cleaned_data['category'].count())
    # print(form)
    # print(form.is_valid())
    if request.method == 'POST' and form.is_valid():
        user = Profile.objects.get(user=request.user)
        group = form.save(commit=False)
        group.save()
        group.prefecture.set(form.cleaned_data['prefecture'])
        group.generation.set(form.cleaned_data['generation'])
        group.category.set(form.cleaned_data['category'])
        group.member.add(user)
        group.administrator.add(user)


        form.save_m2m()

        return redirect(reverse('group:group_detail', kwargs={'group_pk': group.pk}))

        # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納


    # GETのとき

    return render(request, 'group/group_create.html', context)


class GroupCreateDone(LoginRequiredMixin, GetRequestUseIdrMixin,  generic.TemplateView):
    template_name = 'group/group_create_done.html'



def group_detail(request, group_pk, *args, **kwargs):
    context = get_user_id(request, **kwargs)
    template_name = 'group/group_detail.html'
    group = get_object_or_404(Group, pk=group_pk)
    context['object'] = group
    if not group.display:
        return redirect('group:group_not_display')

    posts = group.blog_set.order_by('posted_at')[:5]
    events = group.event_set.order_by('posted_at')[:5]
    members = group.member.all()[:5]
    administrators = group.administrator.all()[:5]

    context['posts'] = posts
    context['events'] = events
    context['members'] = members
    context['administrators'] = administrators



    return render(request, template_name, context)

@group_pk_request_user_is_administrator
def update_group(request, group_pk, *args, **kwargs):
    context = get_user_id(request, **kwargs)

    group = get_object_or_404(Group, pk=group_pk)


    form = GroupCreateForm(request.POST or None, request.FILES or None, instance=group)
    # print(form.prefecture)
    # print(context)
    # context = {}
    context['form'] = form

    if request.method == 'GET':



        # id_category_number = 0
        # category_outdoors = GroupCategory.objects.filter(category_sort='1')
        # category_cultures = GroupCategory.objects.filter(category_sort='2')
        # category_socials = GroupCategory.objects.filter(category_sort='3')

        checked_category = list(group.category.values_list('id', flat=True))
        checked_prefecture = list(group.prefecture.values_list('id', flat=True))
        print(checked_category)
        context['checked_prefecture'] = checked_prefecture
        context['checked_category'] = checked_category

        # group = get_object_or_404(Group, pk=group_pk)
        # prefecture_list = []
        # for prefecture in group.prefecture.all():
        #     prefecture_list.append(int(prefecture.prefecture))
        # context['prefecture_list'] = prefecture_list

        # print(checked_category)
        # category_outdoor_form = []
        # for category_outdoor in category_outdoors:
        #     if str(id_category_number + 1) in checked_category:
        #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                      + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                      + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" checked >' \
        #                                      + category_outdoor.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                      + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                      + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" >' \
        #                                      + category_outdoor.__str__() + '</label>')
        #         id_category_number += 1
        #
        # category_culture_form = []
        # for category_culture in category_cultures:
        #     if str(id_category_number + 1) in checked_category:
        #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                      + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                      + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" checked>' \
        #                                      + category_culture.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                      + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                      + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '">' \
        #                                      + category_culture.__str__() + '</label>')
        #         id_category_number += 1
        #
        # category_social_form = []
        # for category_social in category_socials:
        #     if str(id_category_number + 1) in checked_category:
        #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                     + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                     + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" checked>' \
        #                                     + category_social.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                     + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1)
        #                                     + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" >' \
        #                                     + category_social.__str__() + '</label>')
        #         id_category_number += 1
        #
        # context['category_outdoor_form'] = category_outdoor_form
        # context['category_culture_form'] = category_culture_form
        # context['category_social_form'] = category_social_form


    if request.method == 'POST':
        # id_category_number = 0
        # category_outdoors = GroupCategory.objects.filter(category_sort='1')
        # category_cultures = GroupCategory.objects.filter(category_sort='2')
        # category_socials = GroupCategory.objects.filter(category_sort='3')
        #
        #
        #
        checked_category = request.POST.getlist('category')
        checked_prefecture = request.POST.getlist('prefecture')
        context['checked_prefecture'] = checked_prefecture
        context['checked_category'] = checked_category
        #
        # group = get_object_or_404(Group, pk=group_pk)
        # prefecture_list = []
        # for prefecture in checked_prefecture:
        #     prefecture_list.append(int(prefecture))
        # print(prefecture_list)
        #
        # context['prefecture_list'] = prefecture_list

        # category_outdoor_form = []
        # for category_outdoor in category_outdoors:
        #     if str(id_category_number+1) in checked_category:
        #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">'\
        #                            + '<input type="checkbox" name="category" value="' + str(id_category_number+1)\
        #                            +'" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked >'\
        #                            + category_outdoor.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_outdoor_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                      + '<input type="checkbox" name="category" value="' + str(
        #             id_category_number + 1) \
        #                                      + '" class ="form-horizontal" id="id_category_' + str(
        #             id_category_number) + '" >' \
        #                                      + category_outdoor.__str__() + '</label>')
        #         id_category_number += 1
        #
        #
        #
        # category_culture_form = []
        # for category_culture in category_cultures:
        #     if str(id_category_number+1) in checked_category:
        #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)\
        #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked>' \
        #                                  + category_culture.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_culture_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1) \
        #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '">' \
        #                                  + category_culture.__str__() + '</label>')
        #         id_category_number += 1
        #
        #
        # category_social_form = []
        # for category_social in category_socials:
        #     if str(id_category_number+1) in checked_category:
        #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                  + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)\
        #                                  + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" checked>' \
        #                                  + category_social.__str__() + '</label>')
        #         id_category_number += 1
        #     else:
        #         category_social_form.append('<li><label for ="id_category_' + str(id_category_number) + '">' \
        #                                     + '<input type="checkbox" name="category" value="' + str(id_category_number + 1)
        #                                     + '" class ="form-horizontal" id="id_category_' + str(id_category_number) + '" >' \
        #                                     + category_social.__str__() + '</label>')
        #         id_category_number += 1
        #
        # context['category_outdoor_form'] = category_outdoor_form
        # context['category_culture_form'] = category_culture_form
        # context['category_social_form'] = category_social_form





        if form.is_valid():

            group = form.save(commit=False)
            group.save()
            group.prefecture.set(form.cleaned_data['prefecture'])
            group.generation.set(form.cleaned_data['generation'])
            group.category.set(form.cleaned_data['category'])



            form.save_m2m()

            return redirect(reverse('group:group_list'))


    return render(request, 'group/group_update.html', context)


class GroupNotDisplay(GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/group_not_display.html'


@login_required
def join_group(request, group_pk, *args, **kwargs):
    context = get_user_id(request, **kwargs)

    join_group = get_object_or_404(Group, pk=group_pk)
    context['join_group'] = join_group

    if request.method == 'GET':
        template_name = 'group/group_join.html'
        return render(request, template_name, context)

    if request.method == 'POST':
        request_user = get_object_or_404(Profile, user=request.user)

        if request_user in join_group.member.all():
            template_name = 'group/group_join_already_member.html'
            return render(request, template_name, context)

        if request_user in join_group.applied_user.all():
            template_name = 'group/group_join_already_appied.html'
            return render(request, template_name, context)


        group_administrators = join_group.administrator.all()

        for group_administrator in group_administrators:
            GroupApplyMessage.objects.create(administrator=group_administrator, applied_user=request_user, group=join_group)

        template_name = 'group/group_join_apply_done.html'
        join_group.applied_user.add(request_user)

        return render(request, template_name, context)





def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    # print(paginator.count)　querysetの数
    # print(paginator.num_pages) 全ページ数
    # print(paginator.page_range) # range(1, 8)のようにページ範囲を返す、1から始まる、全7ページの場合は第2引数は8
    # for i in paginator.page_range:
    #     print(i) とすると 1, 2, 3, 4, 5, 6, 7
    # print(paginator)
    page = request.GET.get('page')
    # print(page) リクエストから送られて来たpageのkeyに対応するvalue、リクエストしたページ番号
    # print(paginator.get_page(page)) # 引数で与えられたページ数のPageオブジェクトを返す、エラーハンドリングあり　例<Page 3 of 5>
    try:
        page_obj = paginator.page(page) # get_pageとほぼ同じ、ただし、エラーハンドリングはしない　<Page 3 of 5>
        # print(page_obj)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj



def group_list(request, *args, **kwargs):

    context = get_user_id(request, **kwargs)
    group_list = Group.objects.all()

    checked_category = request.GET.getlist('ca')
    checked_prefecture = request.GET.getlist('pr')
    checked_generation = request.GET.getlist('ge')

    context['checked_category'] = checked_category
    context['checked_prefecture'] = checked_prefecture
    context['checked_generation'] = checked_generation

    search_word = ''
    try:
        search_word = request.GET['search']
    except KeyError:
        pass

    form = GroupSearchForm(request.GET)
    context['form'] = form
    context['search_word'] = search_word


    if checked_generation:
        for generation_query in checked_generation:
            try:
                query_ge |= Q(generation__generation=generation_query)
            except UnboundLocalError:
                query_ge = Q(generation__generation=generation_query)

        group_list = group_list.filter(query_ge).distinct()


    if checked_prefecture:
        for prefecture_query in checked_prefecture:
            try:
                query_pr |= Q(prefecture__prefecture=prefecture_query)
            except UnboundLocalError:
                query_pr = Q(prefecture__prefecture=prefecture_query)

        group_list = group_list.filter(query_pr).distinct()



    if checked_category:

        for category_query in checked_category:
            try:
                query_ca |=  Q(category__category=category_query)
            except:
                query_ca =  Q(category__category=category_query)



        group_list = group_list.filter(query_ca).distinct()


    if search_word:
        search_word_list = search_word.split()
        for each_word in search_word_list:


            query_search = Q(name__icontains=each_word) |\
                    Q(subtitle__icontains=each_word) | \
                    Q(activity_description__icontains=each_word) | \
                    Q(mood__icontains=each_word) | \
                    Q(welcome_person__icontains=each_word) | \
                    Q(day__icontains=each_word) | \
                    Q(last_comment__icontains=each_word) | \
                    Q(detail_place__icontains=each_word)
            group_list = group_list.filter(query_search)



    # group_list = group_list.order_by('-number_of_members')



    page_obj = paginate_queryset(request, group_list, 15)
    # page = request.GET.getlist('page')

    # print(page_obj.number) 現在のページ番号を返す

    context['group_list'] = page_obj.object_list
    context['page_obj'] = page_obj

    return render(request, 'group/group_list.html', context)



@group_pk_request_user_is_administrator
def approve_applied_user(request, group_pk, user_pk, *args, **kwargs):
    context = get_user_id(request)
    group = get_object_or_404(Group, pk=group_pk)
    profile_user = get_object_or_404(Profile, pk=user_pk)
    form = ApproveOrRefuseUserForm(request.POST or None)
    template_name = 'group/approve_applied_user.html'
    context['username'] = profile_user.user.user_name
    context['group'] = group
    context['form'] = form



    if request.method == 'POST' and form.is_valid():
        choice = form.cleaned_data['choice']
        if choice == '1':
            group.applied_user.remove(profile_user)
            group.member.add(profile_user)
            content = 'おめでとうございます！' + group.name + 'のメンバーとして承認されました。'
            AdminMessage.objects.create(user=profile_user, title='承認結果のお知らせ', content=content)

            return redirect('group:group_list')

        if choice == '2':
            group.applied_user.remove(profile_user)
            content = '審査の結果、' + group.name + 'から承認されませんでした。'
            AdminMessage.objects.create(user=profile_user, title='承認結果のお知らせ', content=content)

            return redirect('group:group_list')



    return render(request, template_name, context)



@login_required
@group_pk_request_user_is_administrator
def apply_administrator(request, user_pk, group_pk, *args, **kwargs):
    context = get_user_id(request, **kwargs)
    profile_user = get_object_or_404(Profile, pk=user_pk)
    group = get_object_or_404(Group, pk=group_pk)
    context['profile_user'] = profile_user
    context['group'] = group

    form = ApplyAdministratorForm(request.POST or None)
    context['form'] = form

    template_name = 'group/apply_add_administrator.html'

    if request.method == 'POST' and form.is_valid():
        if profile_user in group.administrator.all():
            template_name = 'group/applied_user_is_already_administrator.html'
            return render(request, template_name, context)
        # group.administrator.add(profile_user)
        group.before_administrator.add(profile_user)
        reason = form.cleaned_data['reason']
        request_user_profile =  get_object_or_404(Profile, user=request.user)
        ApplyAdministratorMessage.objects.create(user=profile_user, administrator=request_user_profile, group=group, reason=reason)
        return redirect(reverse('group:group_list'))

    return render(request, template_name, context)



@login_required
@only_request_user_pk_user
def admit_being_administrator(request, user_pk, group_pk, *args, **kwargs):
    context = get_user_id(request)
    group = get_object_or_404(Group, pk=group_pk)
    profile_user = get_object_or_404(Profile, pk=user_pk)
    form = AdmitOrRefuseBeingAdministratorForm(request.POST or None)
    template_name = 'group/admit_being_administrator.html'
    context['profile_user'] = profile_user
    context['group'] = group
    context['form'] = form

    if profile_user in group.before_administrator.all():

        if request.method == 'POST' and form.is_valid():
            choice = form.cleaned_data['choice']

            if choice == '1':
                if profile_user in group.administrator.all():
                    template_name = 'group/applied_user_is_already_administrator.html'
                    return render(request, template_name, context)

                group.before_administrator.remove(profile_user)
                group.administrator.add(profile_user)

                for group_administrator in group.administrator.all():
                    title = '管理者追加のお知らせ'
                    content = profile_user.user.user_name + 'さんが' + group.name + 'の管理者となりました。'

                    AdminMessage.objects.create(user=group_administrator, title=title, content=content)

                return redirect('group:group_list')

            if choice == '2':
                group.before_administrator.remove(profile_user)
                return redirect('group:group_list')

        return render(request, template_name, context)

    else:
        return HttpResponseForbidden('<h1>403 Forbitten</h1>')





@login_required
@group_pk_request_user_is_administrator
def remove_user_from_group(request, user_pk, group_pk, *args, **kwargs):
    context = get_user_id(request, **kwargs)
    template_name = 'group/remove_user.html'
    profile_user = get_object_or_404(Profile, pk=user_pk)
    group = get_object_or_404(Group, pk=group_pk)
    form = RemoveUseForm(request.POST or None)

    context['profile_user'] = profile_user
    context['group'] = group
    context['form'] = form

    if profile_user in group.administrator.all():
        template_name = 'group/user_is_administrator.html'
        return render(request, template_name, context)
    else:

        if request.method == 'POST' and form.is_valid():
            group.member.remove(profile_user)
            return redirect('group:group_list')


        return render(request, template_name, context)



class GroupMemberList(LoginRequiredMixin, GroupPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'group/group_member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        group_administrators = group.administrator.all().values_list('id')


        members = group.member.all().exclude(id__in=group_administrators)
        # for group_administrator in group_administrators:
        #     print(group_administrator)
        #     delete_members = group.member.exclude(group_administrator)
        # print(delete_members)

        # delete_members = delete_members and group_administrators

        return members

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class GroupAdministratorListForAll(GetRequestUseIdrMixin, generic.ListView):
    template_name = 'group/group_administrator_list_for_all.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        members = group.administrator.all()

        return members

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context



class GroupMemberListForAll(GetRequestUseIdrMixin, generic.ListView):
    template_name = 'group/group_member_list_for_all.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        members = group.member.all()

        return members

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class LeaveGroup(LoginRequiredMixin, RequestUserIsInTheGroup, GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/leave.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        context['user'] = user_profile

        if user_profile in group.administrator.all() and group.administrator.count() <= 1:
            template_name = 'group/cannot_leave.html'
            return render(request, template_name, context)

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        context['user'] = user_profile

        try:
            if self.request.POST['delete'] == 'delete':
                template_name = 'group/leave.html'
                return render(request, self.template_name, context)

        except KeyError:
            pass
        try:
            if self.request.POST['delete_complete'] == 'delete_complete':
                group.member.remove(user_profile)
                if user_profile in group.administrator.all():
                    group.administrator.remove(user_profile)
                    if group.administrator.count() <= 1:
                        group.delete()

                return redirect('group:leave_group_done')

        except KeyError:
            return redirect('group:group_list')


class LeaveGroupDone(LoginRequiredMixin,GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/leave_complete.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().get(request, *args, **kwargs)

class DeleteGroup(LoginRequiredMixin, GroupPkRequestUserIsAdministrator, GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/delete_group.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        context['user'] = user_profile
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        group.delete()

        return redirect('group:delete_group_done')

class DeleteGroupDone(LoginRequiredMixin,GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/delete_group_done.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().get(request, *args, **kwargs)


class ManageGroup(LoginRequiredMixin, GroupPkRequestUserIsAdministrator, GetRequestUseIdrMixin,generic.TemplateView):
    template_name = 'group/managing_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group

        return context



class BelongingGroupList(LoginRequiredMixin, GetRequestUseIdrMixin, generic.ListView):
    template_name = 'group/belonging_group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        user_profile =get_object_or_404(Profile, user=self.request.user)
        groups = Group.objects.filter(member=user_profile)
        return groups

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        managing_groups = Group.objects.filter(administrator=user_profile)
        context['managing_groups'] = managing_groups
        return context


class BelongingGroupInfo(LoginRequiredMixin, GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/belonging_group_info.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        return context


class StopRecruitingMember(LoginRequiredMixin, GroupPkRequestUserIsAdministrator,GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'group/stop_recruiting_member.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        context['group'] = group
        if group.recruit_member:
            return render(request, self.template_name, context)
        else:
            template_name = 'group/resume_recruiting_member.html'
            return render(request, template_name, context)



    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        if group.recruit_member:

            group.recruit_member = False
            group.save()
        else:
            group.recruit_member = True
            group.save()

        return redirect(reverse_lazy('group:managing_group', kwargs={'group_pk': group.pk}))


