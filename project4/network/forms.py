from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': "form-control",
                'row': 2
            })
        }
        labels = {
            'content': 'New Post'
        }
