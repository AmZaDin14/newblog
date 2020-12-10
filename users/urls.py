from django.urls import path
from django.contrib.auth import views as auth_views
from blog.views import author_profile
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<slug:slug>/', author_profile, name='author-profile'),
]