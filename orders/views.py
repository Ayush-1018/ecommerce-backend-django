from rest_framework import generics, permissions
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem
from rest_framework.response import Response


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        with transaction.atomic():
            order = Order.objects.create(user=user)
            total_price = 0

            for item in cart_items:
                product = item.product

                if product.stock < item.quantity:
                    raise Exception("Not enough stock")

                product.stock -= item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price
                )

                total_price += product.price * item.quantity

            order.total_price = total_price
            order.save()

            cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=201)