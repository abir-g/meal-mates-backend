from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Meal, Ingredient
from .serializers import MealSerializer, IngredientSerializer

class MealViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MealSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        meal = get_object_or_404(self.queryset, pk=pk)
        serializer = MealSerializer(meal, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        meal = get_object_or_404(self.queryset, pk=pk)
        ingredients = meal.ingredients.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    