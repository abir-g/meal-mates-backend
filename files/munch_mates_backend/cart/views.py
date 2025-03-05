from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.

class IsCartOwner(BasePermission):
    """
    Custom permission to only allow owners of a cart to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the cart belongs to the current user or session
        if request.user.is_authenticated:
            return obj.user == request.user
        return obj.session_id == request.session.session_key

class CartViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `list()` and `destroy()` actions.
    Custom actions for cart operations.
    """
    serializer_class = CartSerializer
    permission_classes = [IsCartOwner]
    
    def get_queryset(self):
        cart = self.get_or_create_cart()
        return Cart.objects.filter(id=cart.id)

    def perform_create(self, serializer):
        cart = self.get_or_create_cart()
        serializer.instance = cart
        return serializer.instance

    def get_or_create_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_key)
        return cart

    def get_cart_item(self, cart, meal_id):
        """Helper method to get cart item and handle exceptions"""
        try:
            return CartItem.objects.get(cart=cart, meal_id=meal_id), None
        except CartItem.DoesNotExist:
            return None, Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        quantity = int(request.data.get('quantity', 1))

        cart_item, error_response = self.get_cart_item(cart, meal_id)
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart, 
                meal_id=meal_id, 
                quantity=quantity
            )

        return Response(self.get_serializer(cart).data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        
        cart_item, error_response = self.get_cart_item(cart, meal_id)
        if not cart_item:
            return error_response
            
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        cart = self.get_object()
        meal_id = request.data.get('meal_id')
        quantity = int(request.data.get('quantity', 1))

        cart_item, error_response = self.get_cart_item(cart, meal_id)
        if not cart_item:
            return error_response

        cart_item.quantity = quantity
        cart_item.save()
        return Response(self.get_serializer(cart).data)

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        return Response(self.get_serializer(cart).data)
