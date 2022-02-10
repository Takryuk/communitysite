from django import forms

from .models import InnerGroupMessage, EventMessage

class InnerGroupMessageCreateForm(forms.ModelForm):

    class Meta:
        model =InnerGroupMessage
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'style': 'width:80%', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'style': 'width:80%;', 'class': 'form-control'}),
        }


class EventMessageCreateForm(forms.ModelForm):

    class Meta:
        model = EventMessage
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'style': 'width:80%', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'style': 'width:80%;', 'class': 'form-control'}),
        }


