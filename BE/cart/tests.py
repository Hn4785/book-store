from django.test import TestCase


from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from books.models import Book
from .models import Cart, CartItem


class CartAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="cart_customer",
            email="cart_customer@example.com",
            password="CustomerTest123!",
            role=User.Role.CUSTOMER,
        )
        self.other_customer = User.objects.create_user(
            username="cart_other",
            email="cart_other@example.com",
            password="OtherTest123!",
            role=User.Role.CUSTOMER,
        )

        self.book = Book.objects.create(
            title="Django cơ bản",
            author="Nguyen Van A",
            description="Sách kiểm thử",
            price=Decimal("120000.00"),
            stock=10,
            is_active=True,
        )

        self.inactive_book = Book.objects.create(
            title="Sách đã ẩn",
            author="Nguyen Van B",
            price=Decimal("50000.00"),
            stock=5,
            is_active=False,
        )

        self.cart_url = reverse("cart:cart-detail")
        self.add_url = reverse("cart:cart-item-add")

    def authenticate_as(self, user):
        token = RefreshToken.for_user(user).access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_anonymous_user_cannot_view_cart(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_can_view_own_cart(self):
        self.authenticate_as(self.customer)

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], [])
        self.assertEqual(response.data["total_quantity"], 0)
        self.assertEqual(
            response.data["total_price"],
            Decimal("0"),
        )

    def test_view_cart_creates_only_one_cart(self):
        self.authenticate_as(self.customer)

        self.client.get(self.cart_url)
        self.client.get(self.cart_url)

        self.assertEqual(
            Cart.objects.filter(user=self.customer).count(),
            1,
        )

    def test_add_book_to_cart(self):
        self.authenticate_as(self.customer)

        response = self.client.post(
            self.add_url,
            {"book_id": self.book.id, "quantity": 2},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_quantity"], 2)
        self.assertEqual(
            response.data["total_price"],
            Decimal("240000"),
        )
        self.assertEqual(
            CartItem.objects.filter(
                cart__user=self.customer,
                book=self.book,
            ).count(),
            1,
        )

    def test_adding_same_book_increases_quantity(self):
        self.authenticate_as(self.customer)

        self.client.post(
            self.add_url,
            {"book_id": self.book.id, "quantity": 2},
            format="json",
        )
        response = self.client.post(
            self.add_url,
            {"book_id": self.book.id, "quantity": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_quantity"], 5)
        self.assertEqual(
            CartItem.objects.filter(
                cart__user=self.customer,
                book=self.book,
            ).count(),
            1,
        )

    def test_cannot_add_inactive_book(self):
        self.authenticate_as(self.customer)

        response = self.client.post(
            self.add_url,
            {"book_id": self.inactive_book.id, "quantity": 1},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            CartItem.objects.filter(
                cart__user=self.customer,
                book=self.inactive_book,
            ).exists()
        )

    def test_cannot_add_more_than_stock(self):
        self.authenticate_as(self.customer)

        response = self.client.post(
            self.add_url,
            {"book_id": self.book.id, "quantity": 11},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            CartItem.objects.filter(
                cart__user=self.customer,
                book=self.book,
            ).exists()
        )

    def test_update_cart_item_quantity(self):
        cart = Cart.objects.create(user=self.customer)
        item = CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2,
        )
        self.authenticate_as(self.customer)

        response = self.client.patch(
            reverse("cart:cart-item-update", kwargs={"pk": item.id}),
            {"quantity": 4},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)

    def test_cannot_update_other_customers_item(self):
        other_cart = Cart.objects.create(user=self.other_customer)
        item = CartItem.objects.create(
            cart=other_cart,
            book=self.book,
            quantity=2,
        )
        self.authenticate_as(self.customer)

        response = self.client.patch(
            reverse("cart:cart-item-update", kwargs={"pk": item.id}),
            {"quantity": 3},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

    def test_customer_cannot_remove_other_customers_item(self):
        other_cart = Cart.objects.create(user=self.other_customer)
        item = CartItem.objects.create(
            cart=other_cart,
            book=self.book,
            quantity=2,
        )
        self.authenticate_as(self.customer)

        response = self.client.delete(
            reverse("cart:cart-item-remove", kwargs={"pk": item.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertTrue(CartItem.objects.filter(pk=item.pk).exists())

    def test_customer_can_remove_own_item(self):
        cart = Cart.objects.create(user=self.customer)
        item = CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2,
        )
        self.authenticate_as(self.customer)

        response = self.client.delete(
            reverse("cart:cart-item-remove", kwargs={"pk": item.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())

