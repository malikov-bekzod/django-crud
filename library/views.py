from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Book
from .forms import AddBookForm


# Create your views here.
class BookListView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get("search_book_name")
        if search is None:
            books = Book.objects.all()
            context = {"books": books}
            return render(request, "library/book_list.html", context)

        else:
            books = Book.objects.filter(title__icontains=search) | Book.objects.filter(
                description__icontains=search
            )
            context = {"books": books, "search": search}
            return render(request, "library/book_list.html", context)


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        context = {"book": book, "id": id}
        return render(request, "library/book_detail.html", context)


class BookUpdateView(View):
    def get(self, request, id):
        form = AddBookForm()
        book = Book.objects.get(id=id)
        context = {"form": form, "book": book}
        return render(request, "library/book_update.html", context)

    def post(self, request, id):
        book = Book.objects.get(id=id)
        print(request.FILES)
        form = AddBookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list_page")
        else:
            return redirect("home_page_name")

class BookDeleteView(View):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        book.delete()
        return redirect("book_list_page")


class AddBookView(View):
    def get(self,request):
        form = AddBookForm()
        context = {"form":form}
        return render(request,"library/book_add.html", context)

    def post(self,request):
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("book_list_page")
        else:
            return redirect("book_add_page")
