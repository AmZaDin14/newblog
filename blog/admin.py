# Blog Post App Admin Configuration

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


class PostAdmin(SummernoteModelAdmin):
    exclude = ('slug',)
    list_display = ['id', 'title', 'category', 'date_created']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_per_page = 25
    summernote_fields = ('content',)


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'date_created', 'active')
    list_filter = ('active', 'date_created')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)