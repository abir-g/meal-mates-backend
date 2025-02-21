from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework import viewsets
from .models import Meal, Ingredient
from .serializers import MealSerializer

class MealViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = Meal.objects.all()
        return queryset

