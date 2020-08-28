from django.urls import path,include
from django.contrib.auth import views as authviews
from . import views as user_views

app_name = 'user'
urlpatterns = [
    path('signin/',user_views.LoginUserView.as_view(),name = 'signin'),
    path('signup/',user_views.SignUpUser.as_view(),name = 'signup'),
    path('logout/',authviews.LogoutView.as_view(),name = 'logout'),
    path(
        'password-reset/',
        authviews.PasswordResetView.as_view(
            template_name = 'user/password_reset.html'
        ),
        name = 'password_reset'),
    
]