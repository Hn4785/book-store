
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminRole
from .models import Book
from .serializers import BookSerializer


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicBookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author"]

    def get_queryset(self):
        return Book.objects.filter(is_active=True).order_by("id")


class PublicBookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Book.objects.filter(is_active=True)

class AdminBookCreateView(generics.CreateAPIView):
    """ADMIN tạo sách mới."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminRole]


class AdminBookUpdateView(generics.UpdateAPIView):
    """ADMIN cập nhật thông tin sách."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ["patch", "put", "head", "options"]


class AdminBookDeactivateView(APIView):
    """ADMIN ẩn sách, không xóa bản ghi."""

    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Không tìm thấy sách."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not book.is_active:
            return Response(
                {"detail": "Sách đã được ẩn trước đó."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book.is_active = False
        book.save(update_fields=["is_active", "updated_at"])

        return Response(
            {
                "message": "Đã ẩn sách thành công.",
                "id": book.id,
                "is_active": book.is_active,
            },
            status=status.HTTP_200_OK,
        )
