from django import forms

from .models import Event, EventComment
from group.forms import FileInputWithPreview


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'content',
            'prefecture',
            'detail_place',
            'event_day',
            'event_end_day',
            'time_description',
            'image1',
            'image2',
            'image3',
        ]


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
            'prefecture': forms.CheckboxSelectMultiple,
            'event_day': forms.SelectDateWidget,
            'event_end_day': forms.SelectDateWidget,
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail_place': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'time_description': forms.Textarea(attrs={'class': 'form-control'}),
        }



class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'