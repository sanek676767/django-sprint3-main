from django.shortcuts import get_object_or_404, render

from .models import Category, Post

POSTS_LIMIT = 5


def index(request):
    post_list = Post.objects.published()[:POSTS_LIMIT]
    return render(request, "blog/index.html", {"post_list": post_list})


def post_detail(request, id):
    post = get_object_or_404(Post.objects.published(), id=id)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = category.posts.published()

    context = {"category": category, "post_list": post_list}
    return render(request, "blog/category.html", context)
