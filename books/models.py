from django.db import models
from users.models import User

class Catalog(models.Model):
    category = models.CharField(max_length=256)
    genre = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.category} | {self.genre}'


class Author(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    # publisher_id = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    publication_year = models.PositiveSmallIntegerField(
    verbose_name='publication year',
    blank=True,
    null=True,  # если год неизвестен
    help_text='Enter the year of publication')
    cover_image_url = models.ImageField(upload_to='books/')
    catalog_id = models.ForeignKey(Catalog, on_delete=models.PROTECT)
    # review_id = models.ForeignKey(Review, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title} | {self.catalog_id}'

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Книга {self.book.title}'

    def sum(self):
        return  self.quantity * self.book.price


