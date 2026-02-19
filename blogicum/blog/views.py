from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_LIMIT = 5


def get_published_posts():
    return (
        Post.objects.select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .order_by('-pub_date')
    )


def index(request):
    post_list = get_published_posts()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(get_published_posts(), id=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, 
        slug=category_slug, 
        is_published=True
    )
    post_list = get_published_posts().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
