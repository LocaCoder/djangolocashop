from turtledemo.chaos import f
from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import SplitPhoneNumberField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'full_name'
        )

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Password dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserResetPasswordForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'})
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Password dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )


class UserChangeAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'full_name',
            'password',
            'last_login'
        )


class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'image',
            'full_name',
            'bio'
        )
        labels = {
            'bio': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'class': 'input_filed'})
        self.fields["phone_number"].widget.attrs.update({'class': 'input_filed'})
        self.fields["full_name"].widget.attrs.update({'class': 'input_filed'})
        self.fields["bio"].widget.attrs.update({'class': 'input_filed_bio'})


class UserRegisterForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    full_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'FullName'})
    )
    phone_number = forms.CharField(
        label='',
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'PhoneNumber'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone number already exists')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Verify Code'})
    )


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'PhoneNumber'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
  )
