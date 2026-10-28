
from rest_framework import serializers

from .models import Order, OrderItem


class CheckoutSerializer(serializers.Serializer):
    shipping_name = serializers.CharField(max_length=255)
    shipping_phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()

    def validate_shipping_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Tên người nhận không được để trống.")
        return value

    def validate_shipping_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Số điện thoại không được để trống.")
        return value

    def validate_shipping_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Địa chỉ giao hàng không được để trống.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "book_title_snapshot",
            "author_snapshot",
            "unit_price",
            "quantity",
            "subtotal",
        ]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_code",
            "status",
            "shipping_name",
            "shipping_phone",
            "shipping_address",
            "total",
            "items",
            "created_at",
            "updated_at",
            "canceled_at",
        ]
        read_only_fields = fields


class AdminOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
