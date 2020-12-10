from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('blog/', views.PostListView.as_view(), name='blog-home'),
    path('blog/post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('blog/post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog/post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blog/post/new', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about_page, name='about-page')

]