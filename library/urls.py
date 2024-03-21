from django.urls import path
from .views import BookListView,BookDetailView,BookUpdateView,BookDeleteView,AddBookView


urlpatterns = [
    path("", BookListView.as_view(), name="book_list_page"),
    path("<int:id>/", BookDetailView.as_view(), name="book_detail_page"),
    path("add/", AddBookView.as_view(), name="book_add_page"),
    path("update/<int:id>/", BookUpdateView.as_view(), name="book_update_page"),
    path("delete/<int:id>/", BookDeleteView.as_view(), name="book_delete_page"),
]
