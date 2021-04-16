from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.mainpage),
    path('addbook', views.addbook),
    path('books/<int:book_id>', views.bookinfo),
    path('books/<int:book_id>/edit', views.editbook),
    path('books/<int:book_id>/favebook', views.favebook),
    path('books/<int:book_id>/unfavebook', views.unfavebook),
    path('books/<int:book_id>/delete', views.delete),
    path('logout', views.logout),
]