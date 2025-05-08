from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from accounts.models import Seller


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()  # Changed to PositiveIntegerField
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)  # Added for better tracking
    updated_at = models.DateTimeField(auto_now=True)     # Added for better tracking

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle potential duplicates
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{Product.objects.count() + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
