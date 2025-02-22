from django.contrib import admin
from .models import Meal, Ingredient
# Register your models here.

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    list_filter = ('ingredients',)
    search_fields = ('name', 'description')
    list_per_page = 10


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name', 'link')
    list_per_page = 10
