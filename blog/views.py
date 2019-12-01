from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account


# Create your views here.
def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.object.all().filter(email=request.user.email).first()
        print(author)
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, "blog/detail_blog.html", context)


def update_blog_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blogPost = get_object_or_404(BlogPost, slug=slug)

    if blogPost.author != user:
        return HttpResponse("You are not author of this post")

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blogPost)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context["success_message"] = "Updated"

    form = UpdateBlogPostForm(
        initial={
            'title': blogPost.title,
            'body': blogPost.body,
            'image': blogPost.image,
        }
    )

    context['form'] = form

    return render(request, 'blog/update_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.all().filter(
            Q(title__icontains=q),
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))



