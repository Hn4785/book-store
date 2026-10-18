import re

from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import User


class EmailAlreadyExists(APIException):
    """Lỗi khi email đã được sử dụng."""

    status_code = 409
    default_detail = {
        "code": "EMAIL_EXISTS",
        "message": "Email đã được sử dụng.",
    }
    default_code = "EMAIL_EXISTS"


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer đăng ký tài khoản khách hàng."""

    username = serializers.CharField(
        min_length=3,
        max_length=30,
        trim_whitespace=False,
    )

    email = serializers.EmailField(
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def validate_username(self, value):
        # Chỉ chấp nhận chữ cái, chữ số, dấu chấm,
        # dấu gạch dưới và dấu gạch ngang.
        if not re.fullmatch(r"[A-Za-z0-9._-]{3,30}", value):
            raise serializers.ValidationError(
                "Username phải dài 3-30 ký tự và chỉ chứa "
                "chữ cái, chữ số, dấu chấm, '_' hoặc '-'."
            )

        # Kiểm tra trùng username không phân biệt hoa/thường.
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Username đã được sử dụng."
            )

        return value

    def validate_email(self, value):
        # Loại bỏ khoảng trắng và chuẩn hóa chữ thường.
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise EmailAlreadyExists()

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        # Không lấy role từ request.
        # Tài khoản đăng ký công khai luôn là CUSTOMER.
        return User.objects.create_user(
            password=password,
            role=User.Role.CUSTOMER,
            **validated_data,
        )