from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer_list"),
    path("manufacturers/<int:pk>/", ManufacturerDetailView.as_view(), name="manufacturer_detail"),
    path("manufacturers/create/", ManufacturerCreateView.as_view(), name="manufacturer_create"),
    path("manufacturers/<int:pk>/update/", ManufacturerUpdateView.as_view(), name="manufacturer_update"),
    path("manufacturers/<int:pk>/delete/", ManufacturerDeleteView.as_view(), name="manufacturer_delete"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path('', HomeView.as_view(), name='home'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='storeapp/Additional/login.html'), name='login'),
    path("register/", RegisterView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(next_page='storeapp:home'), name='logout'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='order_cancel'),
    path('secret/', SecretView.as_view(), name='secret'),


]

app_name = "storeapp"