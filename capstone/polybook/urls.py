from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('search_book', views.search_book, name='search_book'),
    path('upload_book', views.upload_book, name='upload_book'),
    path('read_book/<int:book_id>', views.read_book, name='read_book'),
    path('save_word', views.save_word, name='save_word')
]
