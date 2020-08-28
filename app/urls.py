from django.urls import path
from . import views as app_views

app_name = 'app'
urlpatterns = [
    path('',app_views.IndexView.as_view(),name = 'home'),
    path('product/<int:pk>/detail/',app_views.ProductDetailView.as_view(),name = 'detail')
]