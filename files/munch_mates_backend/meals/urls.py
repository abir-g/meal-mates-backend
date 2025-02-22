from django.urls import path
from .views import MealViewSet

urlpatterns = [
    path('', MealViewSet.as_view(), name='meal-list'),
    path('<int:pk>/', MealViewSet.as_view(), name='meal-detail'),
]
