from django.contrib import admin
from .models import Topic, Post, Comment, Tag


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "author", "created_at")
    search_fields = ("title", "body")
    list_filter = ("created_at", "topic", "tags")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at", "body_snippet")
    list_filter = ("created_at", "author")

    def body_snippet(self, obj):
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body
  
    body_snippet.short_description = "Comment Preview"

    admin.site.register(Tag)



    

