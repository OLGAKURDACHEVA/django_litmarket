from django.contrib import admin


from books.models import Book, Catalog, Author, Basket

admin.site.register(Book)
admin.site.register(Catalog)
admin.site.register(Author)
admin.site.register(Basket)
