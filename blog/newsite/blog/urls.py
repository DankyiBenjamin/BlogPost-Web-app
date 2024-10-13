from django.urls import path
from . import views
from django.contrib.auth import views as auth
app_name = 'blog'
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('<int:blog_id>/', views.details, name="details"),
    # do for delete and others
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', auth.LogoutView.as_view(next_page="blog:homepage"), name='logout'),
    path('new_blog/', views.create_blog, name="new_blog")
]
