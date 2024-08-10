# django
from django import forms
# local
from .models import Package, Comment
import phonenumber_field


# Third-party
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'id': 'textAreaExample'}),
        }
        labels = {
            'content': ''
        }


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
            'parent'
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'id': 'textAreaExample'}),
        }
        labels = {
            'content': '',
            'parent': ''
        }


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-3", "type": "search", "placeholder": "Search", "aria-label": "Search"}),
        label="",
    )


class SendEmailForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    user_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Message'}))
