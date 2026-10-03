from django.contrib import admin
from .models import Book, Member, Borrowing


admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Borrowing)