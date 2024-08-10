from django.contrib import admin
from .models import Category, Package, Subscription, SubscriptionBuy, Comment, Vote

from mptt.admin import MPTTModelAdmin

admin.site.register(Category, MPTTModelAdmin)


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('id', 'content', 'parent', 'created_at')
    list_filter = ('parent',)
    search_fields = ('content',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)


@admin.register(SubscriptionBuy)
class SubscriptionBuyAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'sub_type',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'package']
