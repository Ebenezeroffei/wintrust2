from django.urls import path
from . import views as control_views

app_name = 'control'
urlpatterns = [
    path('home/',control_views.AdminHomeView.as_view(),name = 'admin_home'),
    path('product/<int:pk>/detail/',control_views.AdminProductDetailView.as_view(),name = 'admin_product_detail'),
    path('',control_views.AdminSigninView.as_view(),name = 'admin_signin'),
    path('admin/logout/',control_views.LogoutAdminView.as_view(),name = 'logout_admin'),
    path('add/product/',control_views.AdminAddProductView.as_view(),name = 'add_product'),
    path('edit/product/<pk>/',control_views.AdminUpdateProductView.as_view(),name = 'update_product'),
    path('delete/product/',control_views.AdminRemoveProductView.as_view(),name = 'delete_product'),
]