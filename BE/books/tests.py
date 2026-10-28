
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer_test",
            email="customer_test@example.com",
            password="CustomerTest123!",
            role=User.Role.CUSTOMER,
        )

        self.admin = User.objects.create_user(
            username="admin_api_test",
            email="admin_api_test@example.com",
            password="AdminTest123!",
            role=User.Role.ADMIN,
            is_staff=True,
        )

        self.book = Book.objects.create(
            title="Django cơ bản",
            author="Nguyen Van A",
            description="Sách kiểm thử",
            price=Decimal("120000.00"),
            stock=10,
            is_active=True,
        )

        self.list_url = reverse("books:book-list")
        self.detail_url = reverse(
            "books:book-detail",
            kwargs={"pk": self.book.pk},
        )
        self.create_url = reverse("books:admin-book-create")
        self.update_url = reverse(
            "books:admin-book-update",
            kwargs={"pk": self.book.pk},
        )
        self.deactivate_url = reverse(
            "books:admin-book-deactivate",
            kwargs={"pk": self.book.pk},
        )

    def authenticate_as(self, user):
        token = RefreshToken.for_user(user).access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_public_list_returns_active_books(self):
        Book.objects.create(
            title="Sách đã ẩn",
            author="Tac gia",
            price=Decimal("50000.00"),
            stock=0,
            is_active=False,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"],
            "Django cơ bản",
        )

    def test_public_detail_returns_active_book(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book.id)

    def test_public_detail_hides_inactive_book(self):
        self.book.is_active = False
        self.book.save()

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_by_title(self):
        response = self.client.get(
            self.list_url,
            {"search": "Django"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_customer_cannot_create_book(self):
        self.authenticate_as(self.customer)

        response = self.client.post(
            self.create_url,
            {
                "title": "Sách mới",
                "author": "Tac gia",
                "price": "50000.00",
                "stock": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)

    def test_anonymous_user_cannot_create_book(self):
        response = self.client.post(
            self.create_url,
            {
                "title": "Sách mới",
                "author": "Tac gia",
                "price": "50000.00",
                "stock": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 1)

    def test_admin_can_create_book(self):
        self.authenticate_as(self.admin)

        response = self.client.post(
            self.create_url,
            {
                "title": "Python cơ bản",
                "author": "Tac gia B",
                "description": "Sách Python",
                "price": "90000.00",
                "stock": 7,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertTrue(
            Book.objects.filter(title="Python cơ bản").exists()
        )

    def test_admin_can_update_book(self):
        self.authenticate_as(self.admin)

        response = self.client.patch(
            self.update_url,
            {"price": "150000.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertEqual(self.book.price, Decimal("150000.00"))

    def test_admin_cannot_create_book_with_negative_price(self):
        self.authenticate_as(self.admin)

        response = self.client.post(
            self.create_url,
            {
                "title": "Sách lỗi",
                "author": "Tac gia",
                "price": "-1000.00",
                "stock": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)

    def test_admin_can_deactivate_book(self):
        self.authenticate_as(self.admin)

        response = self.client.post(self.deactivate_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertFalse(self.book.is_active)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_customer_cannot_deactivate_book(self):
        self.authenticate_as(self.customer)

        response = self.client.post(self.deactivate_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.book.refresh_from_db()
        self.assertTrue(self.book.is_active)
