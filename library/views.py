from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Book, Member, Borrowing


def home(request):
    return render(request, "library/home.html")


def book_list(request):
    books = Book.objects.all().order_by("title")

    return render(
        request,
        "library/book_list.html",
        {"books": books}
    )


def member_list(request):
    members = Member.objects.all().order_by("name")

    return render(
        request,
        "library/member_list.html",
        {"members": members}
    )


def search_books(request):
    query = request.GET.get("q", "").strip()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        ).order_by("title")
    else:
        books = Book.objects.all().order_by("title")

    return render(
        request,
        "library/search.html",
        {
            "books": books,
            "query": query
        }
    )


def borrow_book(request):
    message = ""

    books = Book.objects.filter(available=True).order_by("title")
    members = Member.objects.all().order_by("name")

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        member_id = request.POST.get("member_id")

        book = get_object_or_404(Book, id=book_id)
        member = get_object_or_404(Member, id=member_id)

        if book.available:
            Borrowing.objects.create(
                book=book,
                member=member,
                borrowed_at=timezone.now().date()
            )

            book.available = False
            book.borrow_count += 1
            book.save()

            message = "Book borrowed successfully."

            books = Book.objects.filter(
                available=True
            ).order_by("title")

        else:
            message = "Book is not available."

    return render(
        request,
        "library/borrow.html",
        {
            "books": books,
            "members": members,
            "message": message
        }
    )


def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    borrowing = Borrowing.objects.filter(
        book=book,
        returned_at__isnull=True
    ).first()

    if borrowing:
        borrowing.returned_at = timezone.now().date()
        borrowing.save()

        book.available = True
        book.save()

    return redirect("/books/")


def history(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    member_history = Borrowing.objects.filter(
        member=member
    ).select_related("book").order_by("-borrowed_at")

    return render(
        request,
        "library/history.html",
        {
            "member": member,
            "history": member_history
        }
    )


def history_list(request):
    members = Member.objects.all().order_by("name")

    return render(
        request,
        "library/history_list.html",
        {"members": members}
    )


def statistics(request):
    total_books = Book.objects.count()

    available_books = Book.objects.filter(
        available=True
    ).count()

    borrowed_books = Book.objects.filter(
        available=False
    ).count()

    total_members = Member.objects.count()

    return render(
        request,
        "library/statistics.html",
        {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members
        }
    )


def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        year = request.POST.get("year")

        Book.objects.create(
            title=title,
            author=author,
            year=year
        )

        return redirect("/books/")

    return render(request, "library/book_form.html")


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.year = request.POST.get("year")

        book.save()

        return redirect("/books/")

    return render(
        request,
        "library/book_form.html",
        {"book": book}
    )


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect("/books/")

    return render(
        request,
        "library/book_delete.html",
        {"book": book}
    )