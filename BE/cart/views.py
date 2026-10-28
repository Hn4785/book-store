
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from .models import Cart, CartItem
from .serializers import (CartSerializer, AddCartItemSerializer, CartItemSerializer,)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            book = Book.objects.select_for_update().filter(
                pk=book_id,
                is_active=True,
            ).first()

            if book is None:
                return Response(
                    {"detail": "Sách không tồn tại hoặc đã ngừng kinh doanh."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart, _ = Cart.objects.get_or_create(user=request.user)

            item = CartItem.objects.filter(
                cart=cart,
                book=book,
            ).first()

            current_quantity = item.quantity if item else 0
            new_quantity = current_quantity + quantity

            if new_quantity > book.stock:
                return Response(
                    {"quantity": "Số lượng trong giỏ vượt quá tồn kho."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if item:
                item.quantity = new_quantity
                item.save(update_fields=["quantity", "updated_at"])
            else:
                CartItem.objects.create(
                    cart=cart,
                    book=book,
                    quantity=quantity,
                )

        cart.refresh_from_db()
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )


class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "head", "options"]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def patch(self, request, *args, **kwargs):
        quantity = request.data.get("quantity")

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            return Response(
                {"quantity": "Số lượng phải là số nguyên."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {"quantity": "Số lượng phải lớn hơn hoặc bằng 1."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            item = self.get_queryset().select_for_update().filter(
                pk=kwargs["pk"]
            ).first()

            if item is None:
                return Response(
                    {"detail": "Không tìm thấy sản phẩm trong giỏ hàng."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            book = Book.objects.select_for_update().get(pk=item.book_id)

            if not book.is_active:
                return Response(
                    {"detail": "Sách đã ngừng kinh doanh."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if quantity > book.stock:
                return Response(
                    {"quantity": "Số lượng yêu cầu vượt quá tồn kho."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item.quantity = quantity
            item.save(update_fields=["quantity", "updated_at"])

        return Response(
            CartItemSerializer(item).data,
            status=status.HTTP_200_OK,
        )


class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
