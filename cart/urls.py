from django.urls import path
from .views import CartListCreateView, CartItemDeleteView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart_list_create'),
    path('<int:pk>/', CartItemDeleteView.as_view(), name='cart_delete'),
]