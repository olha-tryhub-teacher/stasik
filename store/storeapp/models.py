from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=180)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('storeapp:category_detail', args=[str(self.id)])


class Manufacturer(models.Model):
    title = models.CharField(max_length=180)
    phone_number = models.CharField(max_length=25)
    address = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=180)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(max_length=2000)
    photo = models.ImageField(upload_to="images/products", verbose_name="photo")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.manufacturer}"


class Order (models.Model):

    STATUS_CHOICES = [
        ("incart", "В корзині"),
        ("new", "Нове"),
        ("processing", "В обробці"),
        ("sent", "Відправлено"),
        ("completed", "Завершено"),
        ("cancelled", "Скасовано"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    def __str__(self):
        return f"order number: {self.id}"


class Order_product (models.Model):
    amount = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.amount}, {self.product}, {self.order}"



