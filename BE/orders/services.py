
from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from books.models import Book
from cart.models import Cart, CartItem

from .models import Order, OrderItem


@transaction.atomic
def checkout(*, user, shipping_name, shipping_phone, shipping_address):
    cart = (
        Cart.objects.select_for_update()
        .filter(user=user)
        .first()
    )

    if cart is None:
        raise ValidationError({"detail": "Giỏ hàng đang trống."})

    cart_items = list(
        CartItem.objects.filter(cart=cart).order_by("book_id", "id")
    )

    if not cart_items:
        raise ValidationError({"detail": "Giỏ hàng đang trống."})

    # Khóa sách theo thứ tự ID để giảm nguy cơ deadlock.
    book_ids = sorted({item.book_id for item in cart_items})
    locked_books = {
        book.id: book
        for book in Book.objects.select_for_update()
        .filter(id__in=book_ids)
        .order_by("id")
    }

    total = Decimal("0.00")
    order_lines = []

    for cart_item in cart_items:
        book = locked_books.get(cart_item.book_id)

        if book is None or not book.is_active:
            raise ValidationError({
                "detail": "Một hoặc nhiều sách không còn kinh doanh."
            })

        if cart_item.quantity > book.stock:
            raise ValidationError({
                "detail": f"Sách '{book.title}' không đủ tồn kho."
            })

        unit_price = book.price
        subtotal = unit_price * cart_item.quantity
        total += subtotal

        order_lines.append({
            "book": book,
            "title": book.title,
            "author": book.author,
            "unit_price": unit_price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal,
        })

    order = Order.objects.create(
        user=user,
        status=Order.Status.PENDING,
        shipping_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address=shipping_address,
        total=total,
    )

    OrderItem.objects.bulk_create([
        OrderItem(
            order=order,
            book=line["book"],
            book_title_snapshot=line["title"],
            author_snapshot=line["author"],
            unit_price=line["unit_price"],
            quantity=line["quantity"],
            subtotal=line["subtotal"],
        )
        for line in order_lines
    ])

    # Trừ tồn kho sau khi đã kiểm tra toàn bộ giỏ hàng.
    for line in order_lines:
        book = line["book"]
        book.stock -= line["quantity"]
        book.save(update_fields=["stock", "updated_at"])

    # Chỉ xóa giỏ hàng sau khi tạo đơn và trừ kho thành công.
    CartItem.objects.filter(cart=cart).delete()

    return order
