from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Meal, Ingredient
from .serializers import MealSerializer

class MealViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()  # Define queryset at class level

    def retrieve(self, request, pk=None):
        meal = get_object_or_404(self.queryset, pk=pk)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    