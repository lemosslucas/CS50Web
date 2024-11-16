
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_new_post", views.add_new_post, name='add_new_post'),
    path("user/<int:user_id>", views.load_user_page, name='load_user_page'),
    path("follow/<int:user_id>/", views.follow, name="follow"),
    path("unfollow/<int:user_id>/", views.unfollow, name="unfollow"),
    path("following_page", views.following_page, name="following_page"),
    path("edit_post/<int:post_id>/", views.edit_post, name='edit_post'),
    path("like_post/<int:post_id>/", views.like_post, name='like_post'),
    path("unlike_post/<int:post_id>/", views.unlike_post, name='unlike_post')
]
