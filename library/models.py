from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    year = models.IntegerField()
    available = models.BooleanField(default=True)
    borrow_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    borrowed_at = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.book}"