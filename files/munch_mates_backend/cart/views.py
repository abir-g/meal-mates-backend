from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.filter(session_id=self.request.session.session_key)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save(session_id=self.request.session.session_key)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart_item = CartItem.objects.get(cart=cart, meal_id=meal_id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, meal_id=meal_id, quantity=quantity)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        
        try:
            cart_item = CartItem.objects.get(cart=cart, meal_id=meal_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart_item = CartItem.objects.get(cart=cart, meal_id=meal_id)
            cart_item.quantity = quantity
            cart_item.save()
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
