from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.Register, name="register"),
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('cart/', views.Cart, name="cart"),
    path('checkout/', views.Checkout, name="checkout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)