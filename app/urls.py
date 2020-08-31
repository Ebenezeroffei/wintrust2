from django.urls import path
from . import views as app_views

app_name = 'app'
urlpatterns = [
    path('',app_views.IndexView.as_view(),name = 'home'),
    path('product/<int:pk>/detail/',app_views.ProductDetailView.as_view(),name = 'detail'),
    path('cart/',app_views.CartView.as_view(),name = 'cart'),
    path('add/cart/',app_views.AddItemToCartView.as_view(),name = 'add_cart'),
]