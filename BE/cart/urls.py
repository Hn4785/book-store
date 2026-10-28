
from django.urls import path

from .views import (
    CartView,
    AddCartItemView,
    UpdateCartItemView,
    RemoveCartItemView,
)

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart-detail"),
    path("items/", AddCartItemView.as_view(), name="cart-item-add"),
    path(
        "items/<int:pk>/",
        UpdateCartItemView.as_view(),
        name="cart-item-update",
    ),
    path(
        "items/<int:pk>/remove/",
        RemoveCartItemView.as_view(),
        name="cart-item-remove",
    ),
]
