from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    publisher_brand = models.CharField(max_length=200,blank=True,)

    class Meta:
        verbose_name = 'Publisher'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} | {self.publisher_brand}'

class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    publication_year = models.PositiveSmallIntegerField(
        verbose_name='publication year',
        blank=True,
        null=True,
        help_text='Enter the year of publication'
    )
    cover_image_url = models.ImageField(upload_to='books/')
    catalog_id = models.ForeignKey(Catalog, on_delete=models.PROTECT)
    COVER_TYPES = [
        ('hard', 'Твёрдая обложка'),
        ('soft', 'Мягкая обложка'),
        ('special', 'Специальная обложка'),
    ]

    AGE_RESTRICTIONS = [
        (0, '0+'),
        (6, '6+'),
        (12, '12+'),
        (16, '16+'),
        (18, '18+'),
    ]

    age_restriction = models.IntegerField(
        choices=AGE_RESTRICTIONS,
        default=0,validators=[MinValueValidator(0), MaxValueValidator(18)]
    )

    cover_type = models.CharField(max_length=10,choices=COVER_TYPES,default='hard'
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    publisher_brand = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Book'

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
        return self.quantity * self.book.price


class MyBooks(models.Model):
    """Модель для хранения книг пользователя в закладках"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_books')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='in_my_books')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Моя книга'
        verbose_name_plural = 'Мои книги'
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"