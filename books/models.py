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

    def get_avg_rating(self):
        reviews = self.reviews.filter(rating__isnull=False)
        if reviews.exists():
            return round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0.0

    def get_reviews_count(self):
        return self.reviews.filter(rating__isnull=False).count()

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_books')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='in_my_books')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Моя книга'
        verbose_name_plural = 'Мои книги'
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    PAYMENT_METHODS = [
        ('card', 'Картой онлайн'),
        ('cash', 'Наличными'),
        ('sbp', 'СБП'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_point = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    comment = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(
                order_number__startswith=date_str
            ).order_by('-order_number').first()

            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.order_number = f"{date_str}-{self.user.id}-{new_num:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ № {self.order_number} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.book.price
        super().save(*args, **kwargs)

    def sum(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.book.title} x{self.quantity}"

class BookOfTheMonth(models.Model):
    MONTH_CHOICES = [
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь'),
        (11, 'Ноябрь'),
        (12, 'Декабрь'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_of_month')
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name='Месяц')
    year = models.PositiveIntegerField(verbose_name='Год')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга месяца'
        verbose_name_plural = 'Книги месяца'
        unique_together = ['month', 'year']

    def __str__(self):
        month_name = dict(self.MONTH_CHOICES)[self.month]
        return f"{self.book.title} - {month_name} {self.year}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.rating}'