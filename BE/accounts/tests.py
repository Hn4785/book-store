
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegisterAPITests(APITestCase):
    URL = "/api/v1/auth/register"

    def test_register_success(self):
        response = self.client.post(
            self.URL,
            {
                "username": "new_customer",
                "email": "NEW@EXAMPLE.COM",
                "password": "TestPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "new_customer")
        self.assertEqual(response.data["email"], "new@example.com")
        self.assertEqual(response.data["role"], "CUSTOMER")
        self.assertNotIn("password", response.data)

        user = User.objects.get(username="new_customer")
        self.assertTrue(user.check_password("TestPass123"))
        self.assertEqual(user.role, User.Role.CUSTOMER)

    def test_register_email_already_exists(self):
        User.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password="TestPass123",
        )

        response = self.client.post(
            self.URL,
            {
                "username": "another_user",
                "email": " EXISTING@EXAMPLE.COM ",
                "password": "TestPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data["code"], "EMAIL_EXISTS")

    def test_register_password_too_short(self):
        response = self.client.post(
            self.URL,
            {
                "username": "short_pass_user",
                "email": "shortpass@example.com",
                "password": "1234567",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(
            User.objects.filter(username="short_pass_user").exists()
        )

    def test_register_invalid_username(self):
        response = self.client.post(
            self.URL,
            {
                "username": "user@123",
                "email": "invaliduser@example.com",
                "password": "TestPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_cannot_assign_admin_role(self):
        response = self.client.post(
            self.URL,
            {
                "username": "public_user",
                "email": "publicuser@example.com",
                "password": "TestPass123",
                "role": "ADMIN",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role"], "CUSTOMER")

    def test_register_duplicate_username_case_insensitive(self):
        User.objects.create_user(
            username="ExistingName",
            email="existingname@example.com",
            password="TestPass123",
        )

        response = self.client.post(
            self.URL,
            {
                "username": "existingname",
                "email": "different@example.com",
                "password": "TestPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
