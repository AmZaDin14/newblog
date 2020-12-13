from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'id': 'Login'}


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun {username} telah dibuat. Anda bisa login sekarang')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'id': 'Register'
    }
    return render(request, 'users/register.html', context)


@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Akun {request.user.username} telah diupdate')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


class DashboardView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 6
    template_name = 'users/dashboard.html'
    extra_context = {
        'title': 'Dashboard'
    }

    def get_queryset(self):
        return Post.objects.filter(status=1).filter(author=self.request.user)
