
from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Chỉ cho phép người dùng đã đăng nhập có role ADMIN.
    """

    message = "Bạn không có quyền thực hiện thao tác này."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and getattr(user, "role", None) == "ADMIN"
        )
