
from rest_framework import serializers

from books.models import Book
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(
        source="book.title",
        read_only=True,
    )
    book_author = serializers.CharField(
        source="book.author",
        read_only=True,
    )
    book_price = serializers.DecimalField(
        source="book.price",
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "book",
            "book_title",
            "book_author",
            "book_price",
            "quantity",
            "subtotal",
        ]
        read_only_fields = [
            "id",
            "book_title",
            "book_author",
            "book_price",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.book.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(
            (item.book.price * item.quantity for item in obj.items.all()),
            start=0,
        )


class AddCartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value, is_active=True)
        except Book.DoesNotExist:
            raise serializers.ValidationError(
                "Sách không tồn tại hoặc đã ngừng kinh doanh."
            )

        self.context["book"] = book
        return value

    def validate(self, attrs):
        book = self.context["book"]
        quantity = attrs["quantity"]

        if quantity > book.stock:
            raise serializers.ValidationError({
                "quantity": "Số lượng yêu cầu vượt quá tồn kho."
            })

        return attrs
