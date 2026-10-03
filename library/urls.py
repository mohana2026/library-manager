from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:book_id>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:book_id>/delete/", views.book_delete, name="book_delete"),

    path("members/", views.member_list, name="member_list"),

    path("search/", views.search_books, name="search_books"),

    path("borrow/", views.borrow_book, name="borrow_book"),

    path("return/<int:book_id>/", views.return_book, name="return_book"),

    path("history/", views.history_list, name="history_list"),
    path("history/<int:member_id>/", views.history, name="history"),

    path("statistics/", views.statistics, name="statistics"),
]