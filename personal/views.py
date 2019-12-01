from django.shortcuts import render
from blog.models import BlogPost
from operator import attrgetter
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from blog.views import get_blog_queryset

# Create your views here.

BLOG_POST_PER_PAGE = 10


def home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blogPosts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blogPostsPaginator = Paginator(blogPosts, BLOG_POST_PER_PAGE)

    try:
        blogPosts = blogPostsPaginator.page(page)
    except PageNotAnInteger:
        blogPosts = blogPostsPaginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blogPosts = blogPostsPaginator.page(blogPostsPaginator.num_pages)

    context["blog_posts"] = blogPosts

    return render(request, "personal/home.html", context)
