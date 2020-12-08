from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CommentForm, PostForm
from users.forms import UserAuthenticationForm


def home_page(request):
    featured_post = Post.objects.get(featured=True)
    context = {
        'id': 'Home Page',
        'post': featured_post
    }
    return render(request, 'homepage.html', context)


def blog_home(request):
    post_list = Post.objects.all()
    form = UserAuthenticationForm()
    context = {
        'id': 'Post List',
        'title': 'Blog Home',
        'post_list': post_list,
        'form': form
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Anda berhasil Login')
            return redirect('blog-home')
        else:
            messages.warning(request, 'Login GAGAL! Silahkan periksa kembali')
            return redirect('blog-home')

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def author_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'id': 'Author Profile',
        'title': user.username,
        'user': user
    }

    return render(request, 'blog/authorprofile.html', context)
