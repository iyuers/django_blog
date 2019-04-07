from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import *


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'qq', 'email']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'click_count')
    list_display_links = ('title', 'desc')
    list_editable = ('click_count', )
    list_filter = ('title', )
    search_fields = ('title', 'content')

    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend', 'user', 'category', 'tag'),
        }),
    )

    class Media:
        js = (
            '/static/kindeditor/kindeditor-min.js',
            '/static/kindeditor/lang/zh_CN.js',
            '/static/kindeditor/config.js'
    )


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    pass


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    pass




