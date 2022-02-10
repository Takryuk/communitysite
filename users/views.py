from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)


from group.models import Group
from message.models import AdminMessage

from .forms import (CustomUserCreationForm,
                    LoginForm,
                    MyPasswordChangeForm,
                    MyPasswordResetForm,
                    MySetPasswordForm,
                    EmailChangeForm,
                    UserNameChangeForm,
                    ProfileForm
                    )
from .models import CustomUser, Profile
from .mixins import GetRequestUseIdrMixin, RequestUserOnlyMixin, SuperuserNotDisplayMixin

from datetime import date

User = get_user_model()

def home(request):
    return render(request, 'your_app/home.html')


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('')
#     template_name = 'users/signup.html'
class UserCreate(GetRequestUseIdrMixin, generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('users/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('users/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('users:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'users/user_create_done.html'



class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'users/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()

                    Profile.objects.create(user=user, sex='N/A')
                    user_profile = get_object_or_404(Profile, user=user)
                    title = 'ようこそ' + user.user_name + 'さん!'
                    content = 'この度はご登録ありがとうございます。' \
                              '\nより質の高いユーザー環境を提供するため、プロフィールの記入をご協力頂いております。' \
                              '\nお手数ですが、「ユーザー設定」からプロフィールの記入をよろしくお願い致します。'
                    AdminMessage.objects.create(user=user_profile, title=title, content=content)


                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()



class UserDetail(SuperuserNotDisplayMixin, GetRequestUseIdrMixin, generic.DetailView):
    model = Profile
    template_name = 'users/user_profile.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class Login(GetRequestUseIdrMixin, LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'users/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'users/top.html'


class PasswordChange(GetRequestUseIdrMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'


class PasswordChangeDone(GetRequestUseIdrMixin, PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'users/password_change_done.html'


class PasswordReset(GetRequestUseIdrMixin,PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'users/mail_template/password_reset/subject.txt'
    email_template_name = 'users/mail_template/password_reset/message.txt'
    template_name = 'users/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')





class PasswordResetDone(GetRequestUseIdrMixin, PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'users/password_reset_done.html'




class PasswordResetConfirm(GetRequestUseIdrMixin, PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'users/password_reset_complete.html'




class EmailChange(LoginRequiredMixin, GetRequestUseIdrMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'users/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject_template = get_template('users/mail_template/email_change/subject.txt')
        subject = subject_template.render(context)
        message_template = get_template('users/mail_template/email_change/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)

        return redirect('users:email_change_done')


class EmailChangeDone(LoginRequiredMixin, GetRequestUseIdrMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'users/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin,GetRequestUseIdrMixin,  generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'users/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)



class UserNameChange(LoginRequiredMixin, GetRequestUseIdrMixin, generic.FormView):
    form_class = UserNameChangeForm
    template_name = 'users/username_change.html'

    def form_valid(self, form):
        username = form.cleaned_data['user_name']
        user = self.request.user
        user.user_name = username
        user.save()

        return redirect(reverse_lazy('users:user_detail', kwargs={'pk': user.profile_set.pk}))


class ProfileChange(LoginRequiredMixin, GetRequestUseIdrMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_change.html'

    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'pk': self.kwargs['pk']})


class AccountDelete(LoginRequiredMixin, GetRequestUseIdrMixin,generic.TemplateView):
    template_name = 'users/account_delete.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        groups = Group.objects.filter(administrator=user_profile)
        administrator_count_list = []
        only_one_administrator_group_list = []
        for group in groups:
            administrator_count_list.append(group.administrator.count())
            if group.administrator.count() <= 1:
                only_one_administrator_group_list.append(group)
                print(only_one_administrator_group_list)
        context['only_one_administrator_group_list'] = only_one_administrator_group_list

        if min(administrator_count_list) <= 1:
            template_name = 'users/cannot_delete.html'
            return render(request, template_name, context)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.POST['delete'] == 'delete':
                user = request.user
                context['user'] = user
                return render(request, self.template_name, context)

        except KeyError:
            pass
        try:
            if self.request.POST['delete_complete'] == 'delete_complete':
                user_profile = get_object_or_404(Profile, user=self.request.user)
                groups = Group.objects.filter(administrator=user_profile)
                for group in groups:
                    if group.administrator.count() <= 1:
                        print(group)
                        group.delete()
                get_object_or_404(CustomUser, pk=request.user.pk).delete()
                template_name = 'users/delete_complete.html'
                return render(request, template_name, context)

        except KeyError:
            return redirect('group:group_list')


class UserConfig(LoginRequiredMixin, GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'users/user_config.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        context['user_profile'] = user_profile
        return context


class TermsOfService(GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'users/terms_of_service.html'


class PrivacyPolicy(GetRequestUseIdrMixin, generic.TemplateView):
    template_name = 'users/privacy_policy.html'
