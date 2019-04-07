from django import forms
from blog.models import Comment, User
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    url = forms.URLField(required=False, label='个人网页地址')

    class Meta:
        model = Comment
        fields = ('username', 'email', 'url', 'content')

        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'height': '300px', 'width': '700px'}}),
            'username': forms.TextInput(attrs={'class': 'mb-3'}),
            'email': forms.TextInput(attrs={'class': 'mb-3'}),
            'url': forms.TextInput(attrs={'class': 'mb-3'}),
        }


# 定义用户表单
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'url', 'avatar', )

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username', 'class': 'mb-3'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'mb-3'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class': 'mb-3'}),
            'url': forms.URLInput(attrs={'placeholder': 'url', 'class': 'mb-3'}),
        }
