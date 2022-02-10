from django import forms

from .models import Blog, BlogComment
from group.forms import FileInputWithPreview


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image1', 'image2', 'image3']


        widgets = {
            'image1': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
            'image2': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
            'image3': FileInputWithPreview(attrs={
                'class': "form-control-file",
            }),
            'content': forms.Textarea(attrs={'style': 'width:80%;', 'class': 'form-control'}),
            'title': forms.Textarea(attrs={'style': 'width:80%; height:8vmax;', 'class': 'form-control title'}),

        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'