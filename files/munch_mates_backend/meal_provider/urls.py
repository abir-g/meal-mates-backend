from django.urls import path, include
from .views import MealViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'meals', MealViewSet, basename='meals')

urlpatterns = [
    path('', include(router.urls)),\
    path('meal/<int:pk>/', MealViewSet.as_view({'get': 'retrieve'}), name='meal-detail'),
    
]
