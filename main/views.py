# django
from xml.etree.ElementPath import get_parent_map
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail
# local
from accounts.models import User
from .forms import Comment, CommentCreateForm, ReplyCommentForm, SearchForm, SendEmailForm
from .models import Package, Category, Subscription, SubscriptionBuy, Vote
# Third-party
from botocore import useragent


class HomePageView(View):
    def get(self, request):
        packages_free = Package.objects.filter(available=True, is_premium=False)
        packages_premium = Package.objects.filter(available=True, is_premium=True)
        sub = Subscription.objects.filter(available=True)
        form = SendEmailForm
        return render(request, 'main/index.html',
                      {'packages_free': packages_free, 'packages_premium': packages_premium, 'sub': sub, 'form': form})


class PackageDetailView(LoginRequiredMixin, View):
    form_class = CommentCreateForm
    form_class_reply = ReplyCommentForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package_instance = None

    def setup(self, request, *args, **kwargs):
        self.package_instance = get_object_or_404(Package, pk=kwargs['package_id'], slug=kwargs['package_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        can_like = False
        sub = False
        packages_premium = Package.objects.filter(available=True, is_premium=True, id=kwargs['package_id'])
        packages_free = Package.objects.filter(available=True, is_premium=False, id=kwargs['package_id'])
        packages = Package.objects.get(id=kwargs['package_id'])
        if request.user.is_authenticated and not SubscriptionBuy.objects.filter(user=request.user) and packages_premium:
            messages.error(request, 'you dont see this blog')
            return redirect('main:main')
        if request.user.is_authenticated and self.package_instance.user_can_like(request.user):
            can_like = True

        return render(request, 'main/detail.html',
                      {'posts': self.package_instance, 'comments': comments, 'forms': self.form_class()
                          , 'reply_form': self.form_class_reply(), 'can_like': can_like, 'packages_free': packages_free,
                       'packages_premium': packages_premium, 'sub': sub, 'packages': packages})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            new_comment = forms.save(commit=False)
            new_comment.user = request.user
            new_comment.package = self.package_instance
            new_comment.save()
            messages.success(request, 'Your Comment submitted successfully !')
        return redirect('main:package_detail', self.package_instance.id, self.package_instance.slug)


class PackageReplyCommentView(LoginRequiredMixin, View):
    form_class = ReplyCommentForm

    def post(self, request, package_id, comment_id):
        package = get_object_or_404(Package, id=package_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.package = package
            reply.save()
            messages.success(request, 'your reply submited successfully..')
        return redirect('main:package_detail', package.id, package.slug)


class ShowPackagesView(View):
    def get(self, request, category_name=None):
        packages_free = Package.objects.filter(available=True, is_premium=False)
        categories = Category.objects.all()
        form = SearchForm()
        packages_premium = Package.objects.filter(available=True, is_premium=True)
        if 'search' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                packages_premium = Package.objects.filter(Q(name__icontains=cd) | Q(description__in=cd),
                                                          is_premium=True)
                packages_free = Package.objects.filter(Q(name__icontains=cd) | Q(description__in=cd), is_premium=False)

        if category_name:
            category = Category.objects.get(name=category_name)
            packages_free = packages_free.filter(category=category)
            packages_premium = packages_premium.filter(category=category)
        return render(request, 'package/show_packages.html', {
            'packages_free': packages_free,
            'packages_premium': packages_premium,
            'categories': categories,
            'form': form})


class PackageSaveView(View):
    def get(self, request, package_id):
        package = get_object_or_404(Package, id=package_id)
        like = Vote.objects.filter(package=package, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post...', 'danger')
        else:
            Vote.objects.create(package=package, user=request.user)
            messages.success(request, 'you saved this post ')
        return redirect('main:package_detail', package.id, package.slug)


class PackageUnSaveView(View):
    def get(self, request, package_id):
        package = get_object_or_404(Package, id=package_id)
        saved = Vote.objects.filter(package=package, user=request.user)
        if saved.exists():
            saved.delete()
            messages.success(request, 'you un saved this post')
            return redirect('main:package_detail', package.id, package.slug)


class SendEmailView(View):
    def post(self, request):
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['subject'], cd['message'], 'amir1386abbas4838@gmail.com', [cd['user_email']])
            messages.success(request, 'Send Email successfully !')
            return redirect('main:main')
        messages.error(request, 'Send Email Error !')
        return redirect('main:main')