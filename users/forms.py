from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,

)
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


from group.forms import FileInputWithPreview
from .models import CustomUser, Profile


User = get_user_model()



# class MinimumLengthValidator:
#     def __init__(self, min_length=8):
#         self.min_length = min_length
#
#     # def validate(self, password, user=None):
#     #     if len(password) < self.min_length:
#     #         raise ValidationError(
#     #             _("This password must contain at least %(min_length)d characters."),
#     #             code='password_too_short',
#     #             params={'min_length': self.min_length},
#     #         )
#
#     def get_help_text(self):
#         return _(
#             "Your password must contain at least %(min_length)d characters."
#             % {'min_length': self.min_length}
#         )

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(required=True, label='メールアドレス', help_text='あなたのメールアドレスを入力してください。')


    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('user_name', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認用）'
        self.fields['user_name'].error_messages = {'max_length': 'ニックネームが30文字を超えています'}
        self.fields['email'].error_messages = {'unique': 'そのメールアドレスは既に使用されています'}
        # self.fields['username'].label = 'ニックネーム'
        # print(self.fields['password2'].error_messages)



        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'

        for fieldname in ['user_name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    # def clean_login_id(self):
    #     login_id = self.cleaned_data['login_id']
    #     if len(login_id) < 6:
    #         raise forms.ValidationError('ログインIDは6文字以上にしてください。')
    #     return login_id
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        # if len(password2) < 8:
        #     raise forms.ValidationError("パスワードは8文字以上にしてください")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")

        return password2

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')




class LoginForm(AuthenticationForm):
    # email = forms.CharField(required=True, label='メールアドレス', help_text='あなたのメールアドレスを入力してください。')
    # class Meta:
    #     model = CustomUser
    #     fields = ('email', 'password',)



    def __init__(self, *args, **kwargs):
        # print(self.fields)
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'パスワード'


        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'
            field.widget.attrs['placeholder'] = field.label

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        # print(self.cleaned_data)
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        # print(CustomUser.objects.first().password)
        # user = CustomUser.objects.filter(email=email, password=password)
        # print(user)
        try:
            user = CustomUser.objects.get(email=email)
            # print(user)
            if user.is_superuser:
                raise ValidationError('正しいメールアドレスとパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。。')
        except ObjectDoesNotExist:
            pass
        return cleaned_data


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserNameChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('user_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('profile', 'sex', 'age', 'twitter_link','facebook_link', 'instagram_link', 'origin')

        widgets = {
            'profile': forms.Textarea(attrs={'class': 'form-control'}),
            'sex': forms.RadioSelect(),
            'age': forms.NumberInput(attrs={'class': 'form-horizontal'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-control'}),
            'origin': FileInputWithPreview(attrs={'class': "form-control-file"})
        }


