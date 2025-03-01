from rest_framework import serializers

from meal_provider.models import Meal
from .models import Cart, CartItem
from meal_provider.serializers import MealSerializer

class CartItemSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)
    meal_id = serializers.PrimaryKeyRelatedField(
        source='meal', write_only=True, 
        queryset=Meal.objects.all()
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'meal', 'meal_id', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'items', 'total_items', 
                 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user', 'session_id', 'created_at', 'updated_at']

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.items.all()) 