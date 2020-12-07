from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from .forms import CommentForm


def home_page(request):
    featured_post = Post.objects.get(featured=True)
    context = {
        'id': 'Home Page',
        'post': featured_post
    }
    return render(request, 'homepage.html', context)


def blog_home(request):
    post_list = Post.objects.all()
    context = {
        'id': 'Post List',
        'title': 'Blog Home',
        'post_list': post_list
    }
    return render(request, 'blog/postlist.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'id': 'Post Detail',
        'title': post.title,
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'blog/postdetail.html', context)


def author_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'id': 'Author Profile',
        'title': user.username,
        'user': user
    }

    return render(request, 'blog/authorprofile.html', context)
