from django.urls import path
from . import views as app_views

app_name = 'app'
urlpatterns = [
    path('',app_views.IndexView.as_view(),name = 'home'),
    path('product/<int:pk>/detail/',app_views.ProductDetailView.as_view(),name = 'detail'),
    path('cart/',app_views.CartView.as_view(),name = 'cart'),
    path('add/cart/',app_views.AddItemToCartView.as_view(),name = 'add_cart'),
    path('decrease/cart/',app_views.DecreaseCartItemQuantityView.as_view(),name = 'decrease'),
    path('increase/cart/',app_views.IncreaseCartItemQuantityView.as_view(),name = 'increase'),
    path('delete/cart/',app_views.DeleteCartItemView.as_view(),name = 'delete'),
    path('checkout/',app_views.CheckoutView.as_view(),name = 'checkout'),
    path('orders/',app_views.OrdersView.as_view(),name = 'orders'),
    path('order/<int:pk>/detail/',app_views.OrderDetailView.as_view(),name = 'order_detail'),
    path('search/',app_views.SearchResultsView.as_view(),name = 'search'),
    path('newsletters/',app_views.NewsLettersView.as_view(),name = 'newsletters')
]
