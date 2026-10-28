
from django.urls import path

from .views import (
    AdminOrderStatusUpdateView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    CancelOrderView,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/cancel/", CancelOrderView.as_view(), name="order-cancel"),
    path("admin/<int:pk>/status/", AdminOrderStatusUpdateView.as_view(),name="admin-order-status",),
]
