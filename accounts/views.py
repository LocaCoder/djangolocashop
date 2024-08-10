# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
# local
from utils import send_otp_code
from .models import User, OtpCode
from .forms import UserRegisterForm, UserLoginForm, VerifyCodeForm, UserProfileChangeForm, UserResetPasswordForm, \
    UserChangePasswordForm
from main.models import Vote, SubscriptionBuy
# Third-party

import random


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_register_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we send you a code ', 'success')
            return redirect('accounts:user_verify')

        return render(request, self.template_name, {'form': form})


class UserVerifyView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        user_session = request.session['user_register_info']
        form = self.form_class
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        return render(request, 'accounts/verify.html', {'form': form, 'code': code_instance})

    def post(self, request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    user_session['phone_number'],
                    user_session['email'],
                    user_session['full_name'],
                    user_session['password']
                )
                code_instance.delete()
                messages.success(request, 'You Regisered', 'success')
                return redirect('main:main')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:user_verify')
        return redirect('main:main')


class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                phone_number=cd['phone_number'],
                password=cd['password']
            )
            if user:
                login(request, user)
                messages.success(request, 'You Loged in', 'success')
                return redirect('main:main')

            messages.error(request, 'this account not found !', 'danger')
            return redirect('accounts:user_login')

        return redirect('main:main')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logouted', 'danger')
        return redirect('main:main')


class UserProfileView(LoginRequiredMixin, View):
    form_class = UserProfileChangeForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        change_password_form = UserChangePasswordForm
        vote = Vote.objects.filter(user=request.user)
        sub_buy = SubscriptionBuy.objects.filter(user=request.user, purchased=True)
        return render(request, 'accounts/profile.html',
                      {'form': form, 'change_password_form': change_password_form, 'vote': vote,
                       'sub_buy': sub_buy})

    def post(self, request):
        form = self.form_class(request.POST or None, files=request.FILES, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile changed !')
            return redirect('accounts:user_profile')
        messages.error(request, 'profile do not changed !')
        return redirect('accounts:user_profile')


class UserResetPasswordView(View):
    form_class = UserResetPasswordForm
    template_name = 'accounts/password_reset.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone_number=cd['phone_number'])
            if user:
                if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
                    messages.error(request, 'password do not same')
                    return redirect(self.template_name)
                user.set_password(cd['password2'])
                user.save()
                messages.success(request, 'Your password Changed')
                return redirect('main:main')
            messages.error(request, 'The information is not correct')
            return redirect(self.template_name)


class UserChangePasswordView(View):
    form_class = UserChangePasswordForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone_number=request.user.phone_number)
            if cd['password1'] and cd['password2'] and cd['password1'] == cd['password2']:
                user.set_password(cd['password2'])
                user.save()
                messages.success(request, 'Your password Changed')
                return redirect("accounts:user_login")
            messages.error(request, 'password do not same')
            return redirect('accounts:user_profile')

        messages.error(request, 'The information is not correct')
        return redirect('accounts:user_profile')
