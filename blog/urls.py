from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('blog/', views.blog_home, name='blog-home'),
    path('blog/<slug:slug>/', views.post_detail, name='post-detail'),

]