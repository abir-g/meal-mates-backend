from django.db import models
from django.contrib.auth import get_user_model
from meal_provider.models import Meal

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    session_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {'User: ' + self.user.username if self.user else 'Session: ' + self.session_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'meal']

    def __str__(self):
        return f"{self.quantity}x {self.meal.name} in Cart {self.cart.id}"

    @property
    def total_price(self):
        return self.quantity * self.meal.price
