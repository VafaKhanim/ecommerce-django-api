# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


# Remove is_seller from UserProfile or keep as legacy field
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=True)
    # is_seller removed or kept as backup


