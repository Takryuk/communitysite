from django import forms


from users.models import Profile
from message.models import ApplyAdministratorMessage

from .models import(
    Group,
    GroupPrefecture,
    GroupGeneration,
    GroupCategory,
)




class BeforeCreateConsentForm(forms.Form):
    consent = forms.BooleanField(required=True, label='同意する')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'


class FileInputWithPreview(forms.ClearableFileInput):
    """プレビュー表示されるinput type=file"""
    template_name = 'widgets/file_input_with_preview.html'

    class Media:
        js = ['js/preview.js']

    def __init__(self, attrs=None, include_preview=True):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' preview-marker'
        else:
            self.attrs['class'] = 'preview-marker'
        self.include_preview = include_preview

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'include_preview': self.include_preview,
        })
        return context

class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        # print(obj)
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj)

class CustomModelChoiceField(forms.models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)
    choices = property(_get_choices,
                       forms.MultipleChoiceField._set_choices)

class GroupCreateForm(forms.ModelForm):

    prefecture = CustomModelChoiceField(widget=forms.CheckboxSelectMultiple, queryset=GroupPrefecture.objects.all())

    category = CustomModelChoiceField(
        queryset=GroupCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )



    class Meta:
        model = Group
        fields = [
            'name',
            'subtitle',
            'activity_description',
            'mood',
            'welcome_person',
            'sex_ratio',
            'number_of_members',
            'max_age',
            'min_age',
            'cost',
            'day',
            'generation',
            'category',
            'last_comment',
            'detail_place',
            'founded_date',
            'prefecture',
            'image1',
            'image2',
            'image3',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'style': 'width:80%','class': 'form-control'}),
            'subtitle': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'activity_description': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'mood': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'welcome_person': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'number_of_members': forms.NumberInput(attrs={'style': 'width:90px;','class': 'form-horizontal'}),
            'founded_date': forms.SelectDateWidget,
            'sex_ratio':forms.Textarea(attrs={'style': 'height:70px; width:40%','class': 'form-control'}),
            'max_age': forms.NumberInput(attrs={'style': 'width:90px;','class': 'form-horizontal'}),
            'min_age': forms.NumberInput(attrs={ 'style': 'width:90px;','class': 'form-horizontal'}),
            'cost': forms.Textarea(attrs={'style': 'height:70px; width:60%','class': 'form-control'}),
            'day': forms.Textarea(attrs={'style': 'height:70px; width:60%','class': 'form-control'}),
            # 'category': CustomModelChoiceField(queryset=GroupCategory.objects.all()),
            'generation': forms.CheckboxSelectMultiple(),
            'prefecture': forms.CheckboxSelectMultiple(),
            'last_comment': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'detail_place': forms.Textarea(attrs={'style': 'width:80%;','class': 'form-control'}),
            'image1': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
            'image2': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
            'image3': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
        }


    def clean_prefecture(self):
        prefecture = []
        try:
            prefecture = self.cleaned_data['prefecture']
        except KeyError:
            pass

        total_prefecture_count = len(prefecture)
        if total_prefecture_count == 0:
            raise forms.ValidationError('都道府県は1つ以上選択してください。')

        if total_prefecture_count > 5:
            raise forms.ValidationError('都道府県は5つ以下にしてください。')
        return prefecture



    def clean_generation(self):
        generation = []
        try:
            generation = self.cleaned_data['generation']
        except KeyError:
            pass

        total_prefecture_count = len(generation)
        if total_prefecture_count == 0:
            raise forms.ValidationError('年代は1つ以上選択してください。')
        return generation


    def clean_category(self):
        total_category_count = 0
        try:
            category = self.cleaned_data['category']
        except KeyError:
            pass
        total_category_count = len(category)
        if total_category_count == 0:
            raise forms.ValidationError('カテゴリーは1つ以上選んでください。')

        if total_category_count > 5:
            raise forms.ValidationError('カテゴリは5つまでにしてください。')
        return category










class GroupSearchForm(forms.Form):
    pr = forms.ModelMultipleChoiceField(
        queryset=GroupPrefecture.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ca = CustomModelChoiceField(
        queryset=GroupCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ge = CustomModelChoiceField(
        queryset=GroupGeneration.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


APPLY_OR_REFUSE_CHOICE = (
    ('1', '承認する'),
    ('2', '承認しない')
)

class ApproveOrRefuseUserForm(forms.Form):
    choice = forms.ChoiceField(choices=APPLY_OR_REFUSE_CHOICE, widget=forms.RadioSelect)

class ApplyAdministratorForm(forms.ModelForm):
    class Meta:
        model = ApplyAdministratorMessage
        fields = ['reason']

        widgets = {
            'reason': forms.Textarea,
        }


ADMIT_OR_REFUSE_CHOICE = (
    ('1', '許諾する'),
    ('2', '断る')
)

class AdmitOrRefuseBeingAdministratorForm(forms.Form):
    choice = forms.ChoiceField(choices=ADMIT_OR_REFUSE_CHOICE, widget=forms.RadioSelect)


class RemoveUseForm(forms.Form):
    consent = forms.BooleanField(required=True, label='同意する')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-horizontal'

