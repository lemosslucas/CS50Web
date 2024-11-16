from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_list', views.create_list, name='create_list'),
    path("<int:listing_id>", views.listing, name='listing'),
    path('new_bid/<int:listing_id>', views.new_bid, name='new_bid'),
    path('watch_list', views.listing_watchlist, name='listing_watchlist'),
    path("<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path('categories', views.listing_categories, name='listing_categories'),
    path('category/<str:category>/', views.index_filter, name='index_filter'),
    path('<int:listing_id>/add_comment', views.add_comment, name='add_comment'),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction")
]
