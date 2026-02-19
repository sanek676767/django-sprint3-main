from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count

from .models import Category, Location, Post

User = get_user_model()



try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, "posts_count")

    @admin.display(description="Постов")
    def posts_count(self, obj):
        return obj.posts_count

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # ВАЖНО: "posts" должно совпадать с related_name у Post.author
        return qs.annotate(posts_count=Count("posts"))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "pub_date",
        "category",
        "location",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = ("is_published", "pub_date", "category")