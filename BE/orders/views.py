
from django.db import transaction
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book

from .models import Order, OrderItem
from .serializers import (CheckoutSerializer, OrderSerializer, AdminOrderStatusSerializer,)
from .services import checkout

from accounts.permissions import IsAdminRole
from .serializers import AdminOrderStatusSerializer

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = checkout(
            user=request.user,
            **serializer.validated_data,
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items")
            .order_by("-created_at", "-id")
        )


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items")
        )


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            order = (
                Order.objects.select_for_update()
                .filter(user=request.user, pk=pk)
                .first()
            )

            if order is None:
                return Response(
                    {"detail": "Không tìm thấy đơn hàng."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if order.status != Order.Status.PENDING:
                return Response(
                    {"detail": "Chỉ có thể hủy đơn đang chờ xác nhận."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            items = list(order.items.all().order_by("book_id"))
            book_ids = sorted({item.book_id for item in items})

            books = {
                book.id: book
                for book in Book.objects.select_for_update()
                .filter(id__in=book_ids)
                .order_by("id")
            }

            for item in items:
                book = books.get(item.book_id)
                if book is not None:
                    book.stock += item.quantity
                    book.save(update_fields=["stock", "updated_at"])

            order.status = Order.Status.CANCELED
            order.canceled_at = timezone.now()
            order.save(update_fields=["status", "canceled_at", "updated_at"])

        order.refresh_from_db()
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK,
        )



class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    ALLOWED_TRANSITIONS = {
        Order.Status.PENDING: {
            Order.Status.CONFIRMED,
            Order.Status.CANCELED,
        },
        Order.Status.CONFIRMED: {
            Order.Status.SHIPPING,
            Order.Status.CANCELED,
        },
        Order.Status.SHIPPING: {
            Order.Status.COMPLETED,
        },
        Order.Status.COMPLETED: set(),
        Order.Status.CANCELED: set(),
    }

    def patch(self, request, pk):
        serializer = AdminOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data["status"]

        with transaction.atomic():
            order = (
                Order.objects.select_for_update()
                .filter(pk=pk)
                .first()
            )

            if order is None:
                return Response(
                    {"detail": "Không tìm thấy đơn hàng."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if new_status not in self.ALLOWED_TRANSITIONS[order.status]:
                return Response(
                    {
                        "detail": (
                            f"Không thể chuyển từ {order.status} "
                            f"sang {new_status}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if new_status == Order.Status.CANCELED:
                items = list(order.items.all().order_by("book_id"))
                book_ids = sorted({item.book_id for item in items})

                books = {
                    book.id: book
                    for book in Book.objects.select_for_update()
                    .filter(id__in=book_ids)
                    .order_by("id")
                }

                for item in items:
                    book = books.get(item.book_id)
                    if book is not None:
                        book.stock += item.quantity
                        book.save(
                            update_fields=["stock", "updated_at"]
                        )

                order.canceled_at = timezone.now()

            order.status = new_status
            update_fields = ["status", "updated_at"]

            if new_status == Order.Status.CANCELED:
                update_fields.append("canceled_at")

            order.save(update_fields=update_fields)

        order.refresh_from_db()
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK,
        )
