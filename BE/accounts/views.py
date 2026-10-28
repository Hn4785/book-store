
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """API đăng ký tài khoản khách hàng."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """API đăng nhập bằng email và mật khẩu."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Tạo access token JWT cho người dùng.
        access_token = RefreshToken.for_user(user).access_token

        return Response(
            {
                "access": str(access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    """API lấy thông tin tài khoản đang đăng nhập."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """API kết thúc phiên làm việc phía client."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Với access token JWT, endpoint này không tự thu hồi token.
        # Client cần xóa access token đang lưu sau khi nhận HTTP 204.
        return Response(status=status.HTTP_204_NO_CONTENT)
