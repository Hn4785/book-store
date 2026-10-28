from django.test import TestCase


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem


User = get_user_model()


class OrderAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password="TestPass123!",
            role="CUSTOMER",
        )
        self.other_customer = User.objects.create_user(
            username="customer2",
            email="customer2@example.com",
            password="TestPass123!",
            role="CUSTOMER",
        )

        self.book = Book.objects.create(
            title="Python cơ bản",
            author="Nguyễn Văn A",
            description="Sách kiểm thử",
            price=Decimal("120000.00"),
            stock=10,
            is_active=True,
        )

        self.cart = Cart.objects.create(user=self.customer)
        self.client.force_authenticate(user=self.customer)

        self.checkout_url = reverse("orders:checkout")
        self.order_list_url = reverse("orders:order-list")

        self.shipping_data = {
            "shipping_name": "Nguyễn Văn B",
            "shipping_phone": "0901234567",
            "shipping_address": "Hà Nội",
        }

    def add_book_to_cart(self, book=None, quantity=1):
        return CartItem.objects.create(
            cart=self.cart,
            book=book or self.book,
            quantity=quantity,
        )

    def create_order(self, user=None, status_value=Order.Status.PENDING):
        user = user or self.customer
        order = Order.objects.create(
            user=user,
            status=status_value,
            shipping_name="Nguyễn Văn B",
            shipping_phone="0901234567",
            shipping_address="Hà Nội",
            total=Decimal("120000.00"),
        )
        OrderItem.objects.create(
            order=order,
            book=self.book,
            book_title_snapshot=self.book.title,
            author_snapshot=self.book.author,
            unit_price=Decimal("120000.00"),
            quantity=1,
            subtotal=Decimal("120000.00"),
        )
        return order

    def test_checkout_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_checkout_rejects_empty_cart(self):
        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_checkout_creates_order_and_deducts_stock(self):
        self.add_book_to_cart(quantity=2)

        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()
        self.assertEqual(order.user, self.customer)
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.total, Decimal("240000.00"))

        item = order.items.get()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Decimal("120000.00"))
        self.assertEqual(item.subtotal, Decimal("240000.00"))
        self.assertEqual(item.book_title_snapshot, "Python cơ bản")
        self.assertEqual(item.author_snapshot, "Nguyễn Văn A")

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 8)
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

    def test_checkout_uses_current_database_price(self):
        self.book.price = Decimal("150000.00")
        self.book.save(update_fields=["price", "updated_at"])
        self.add_book_to_cart(quantity=2)

        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get()
        item = order.items.get()

        self.assertEqual(order.total, Decimal("300000.00"))
        self.assertEqual(item.unit_price, Decimal("150000.00"))
        self.assertEqual(item.subtotal, Decimal("300000.00"))

    def test_checkout_rejects_insufficient_stock_without_changes(self):
        self.add_book_to_cart(quantity=11)

        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 10)
        self.assertTrue(CartItem.objects.filter(cart=self.cart).exists())

    def test_checkout_rejects_inactive_book_without_changes(self):
        self.book.is_active = False
        self.book.save(update_fields=["is_active", "updated_at"])
        self.add_book_to_cart()

        response = self.client.post(
            self.checkout_url,
            self.shipping_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 10)
        self.assertTrue(CartItem.objects.filter(cart=self.cart).exists())

    def test_checkout_rejects_blank_shipping_information(self):
        self.add_book_to_cart()
        data = {
            **self.shipping_data,
            "shipping_name": "   ",
        }

        response = self.client.post(
            self.checkout_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_customer_can_list_only_own_orders(self):
        own_order = self.create_order()
        self.create_order(user=self.other_customer)

        response = self.client.get(self.order_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [item["id"] for item in response.data["results"]] \
            if isinstance(response.data, dict) and "results" in response.data \
            else [item["id"] for item in response.data]

        self.assertIn(own_order.id, returned_ids)
        self.assertEqual(len(returned_ids), 1)

    def test_customer_cannot_view_another_customers_order(self):
        other_order = self.create_order(user=self.other_customer)
        url = reverse("orders:order-detail", kwargs={"pk": other_order.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_can_cancel_pending_order_and_restore_stock(self):
        order = self.create_order()
        self.book.stock = 9
        self.book.save(update_fields=["stock", "updated_at"])

        url = reverse("orders:order-cancel", kwargs={"pk": order.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(order.status, Order.Status.CANCELED)
        self.assertIsNotNone(order.canceled_at)
        self.assertEqual(self.book.stock, 10)

    def test_cancel_order_cannot_restore_stock_twice(self):
        order = self.create_order(status_value=Order.Status.CANCELED)
        order.canceled_at = order.created_at
        order.save(update_fields=["canceled_at"])

        self.book.stock = 9
        self.book.save(update_fields=["stock", "updated_at"])

        url = reverse("orders:order-cancel", kwargs={"pk": order.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 9)

    def test_customer_cannot_cancel_another_customers_order(self):
        order = self.create_order(user=self.other_customer)
        url = reverse("orders:order-cancel", kwargs={"pk": order.pk})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_cannot_cancel_confirmed_order(self):
        order = self.create_order(status_value=Order.Status.CONFIRMED)
        self.book.stock = 9
        self.book.save(update_fields=["stock", "updated_at"])

        url = reverse("orders:order-cancel", kwargs={"pk": order.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 9)

    
    def test_admin_can_confirm_pending_order(self):
        admin = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="TestPass123!",
            role="ADMIN",
        )
        order = self.create_order()
        self.client.force_authenticate(user=admin)

        url = reverse(
            "orders:admin-order-status",
            kwargs={"pk": order.pk},
        )
        response = self.client.patch(
            url,
            {"status": Order.Status.CONFIRMED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CONFIRMED)

    def test_customer_cannot_update_order_status_as_admin(self):
        order = self.create_order()

        url = reverse(
            "orders:admin-order-status",
            kwargs={"pk": order.pk},
        )
        response = self.client.patch(
            url,
            {"status": Order.Status.CONFIRMED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_admin_cannot_skip_order_status(self):
        admin = User.objects.create_user(
            username="admin2",
            email="admin2@example.com",
            password="TestPass123!",
            role="ADMIN",
        )
        order = self.create_order()
        self.client.force_authenticate(user=admin)

        url = reverse(
            "orders:admin-order-status",
            kwargs={"pk": order.pk},
        )
        response = self.client.patch(
            url,
            {"status": Order.Status.COMPLETED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_admin_cannot_update_nonexistent_order(self):
        admin = User.objects.create_user(
            username="admin3",
            email="admin3@example.com",
            password="TestPass123!",
            role="ADMIN",
        )
        self.client.force_authenticate(user=admin)

        url = reverse(
            "orders:admin-order-status",
            kwargs={"pk": 999999},
        )
        response = self.client.patch(
            url,
            {"status": Order.Status.CONFIRMED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_cancel_order_restores_stock_once(self):
        admin = User.objects.create_user(
            username="admin4",
            email="admin4@example.com",
            password="TestPass123!",
            role="ADMIN",
        )
        order = self.create_order()
        self.book.stock = 9
        self.book.save(update_fields=["stock", "updated_at"])
        self.client.force_authenticate(user=admin)

        url = reverse(
            "orders:admin-order-status",
            kwargs={"pk": order.pk},
        )
        response = self.client.patch(
            url,
            {"status": Order.Status.CANCELED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(order.status, Order.Status.CANCELED)
        self.assertIsNotNone(order.canceled_at)
        self.assertEqual(self.book.stock, 10)

        response_again = self.client.patch(
            url,
            {"status": Order.Status.CANCELED},
            format="json",
        )

        self.assertEqual(
            response_again.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 10)

