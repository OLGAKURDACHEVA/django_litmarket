from django.contrib import admin
from books.models import Book, Catalog, Author, Basket, Publisher, MyBooks, BookOfTheMonth

admin.site.register(Book)
admin.site.register(Catalog)
admin.site.register(Author)
admin.site.register(Basket)
admin.site.register(Publisher)
admin.site.register(MyBooks)

@admin.register(BookOfTheMonth)
class BookOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ['book', 'month', 'year', 'is_active']
    list_filter = ['is_active', 'month', 'year']
    search_fields = ['book__title']