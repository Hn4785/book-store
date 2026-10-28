
from django.urls import path

from .views import (
    PublicBookListView,
    PublicBookDetailView,
    AdminBookCreateView,
    AdminBookUpdateView,
    AdminBookDeactivateView,
)

app_name = "books"

urlpatterns = [
    # API công khai
    path("", PublicBookListView.as_view(), name="book-list"),
    path("<int:pk>/", PublicBookDetailView.as_view(), name="book-detail"),

    # API quản trị
    path("admin/", AdminBookCreateView.as_view(), name="admin-book-create"),
    path(
        "admin/<int:pk>/",
        AdminBookUpdateView.as_view(),
        name="admin-book-update",
    ),
    path(
        "admin/<int:pk>/deactivate/",
        AdminBookDeactivateView.as_view(),
        name="admin-book-deactivate",
    ),
]
