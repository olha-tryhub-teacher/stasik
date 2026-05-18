from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Product, Category, Manufacturer, Order, Order_product
from django.db.models import Count
from .mixins import (CreateUpdateMixin, SuccessUrlProductMixin, SuccessUrlCategoryMixin, SuccessUrlManufacturerMixin,
                     SuccessUrlOrderMixin, AdminRequiredMixin)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views import View


class ProductListView(ListView):
    model = Product
    template_name = "storeapp/Product/Product_List.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "storeapp/Product/Product_Detail.html"
    context_object_name = "product"


class ProductCreateView(AdminRequiredMixin, CreateUpdateMixin, SuccessUrlProductMixin, CreateView):
    model = Product
    fields = "__all__"
    template_name = "storeapp/Product/Product_Create.html"
    success_url = reverse_lazy("storeapp:product_list")


class ProductUpdateView(AdminRequiredMixin, CreateUpdateMixin, SuccessUrlProductMixin, UpdateView):
    model = Product
    fields = "__all__"
    template_name = "storeapp/Product/Product_Update.html"
    success_url = reverse_lazy("storeapp:product_list")


class ProductDeleteView(AdminRequiredMixin, SuccessUrlProductMixin, DeleteView):
    model = Product
    template_name = "storeapp/Product/Product_Delete.html"
    success_url = reverse_lazy("storeapp:product_list")


class CategoryListView(ListView):
    model = Category
    template_name = "storeapp/Category/Category_List.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "storeapp/Category/Category_Detail.html"
    context_object_name = "category"

    def get_queryset(self):
        # Додаємо кількість продуктів у кожній категорії
        return Category.objects.annotate(product_count=Count('product'))


class CategoryCreateView(AdminRequiredMixin, CreateUpdateMixin, SuccessUrlCategoryMixin, CreateView):
    model = Category
    fields = "__all__"
    template_name = "storeapp/Category/Category_Create.html"
    success_url = reverse_lazy("storeapp:category_list")


class CategoryUpdateView(AdminRequiredMixin, CreateUpdateMixin, SuccessUrlCategoryMixin, UpdateView):
    model = Category
    fields = "__all__"
    template_name = "storeapp/Category/Category_Update.html"
    success_url = reverse_lazy("storeapp:category_list")


class CategoryDeleteView(AdminRequiredMixin, SuccessUrlCategoryMixin, DeleteView):
    model = Category
    template_name = "storeapp/Category/Category_Delete.html"
    success_url = reverse_lazy("storeapp:category_list")


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = "storeapp/Manufacturer/Manufacturer_List.html"
    context_object_name = "manufacturers"


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = "storeapp/Manufacturer/Manufacturer_Detail.html"
    context_object_name = "manufacturer"


class ManufacturerCreateView(AdminRequiredMixin, CreateUpdateMixin, SuccessUrlManufacturerMixin, CreateView):
    model = Manufacturer
    fields = "__all__"
    template_name = "storeapp/Manufacturer/Manufacturer_Create.html"
    success_url = reverse_lazy("storeapp:manufacturer_list")


class ManufacturerUpdateView(CreateUpdateMixin, SuccessUrlManufacturerMixin, UpdateView):
    model = Manufacturer
    fields = "__all__"
    template_name = "storeapp/Manufacturer/Manufacturer_Update.html"
    success_url = reverse_lazy("storeapp:manufacturer_list")


class ManufacturerDeleteView(SuccessUrlManufacturerMixin, DeleteView):
    model = Manufacturer
    template_name = "storeapp/Manufacturer/Manufacturer_Delete.html"
    success_url = reverse_lazy("storeapp:manufacturer_list")


class OrderListView(ListView):
    model = Order
    template_name = "storeapp/Order/Order_List.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    model = Order
    template_name = "storeapp/Order/Order_Detail.html"
    context_object_name = "order"


class OrderCreateView(CreateUpdateMixin, SuccessUrlOrderMixin, CreateView):
    model = Order
    fields = "__all__"
    template_name = "storeapp/Order/Order_Create.html"
    success_url = reverse_lazy("storeapp:order_list")


class OrderUpdateView(CreateUpdateMixin, SuccessUrlOrderMixin, UpdateView):
    model = Order
    fields = "__all__"
    template_name = "storeapp/Order/Order_Update.html"
    success_url = reverse_lazy("storeapp:order_list")


class OrderDeleteView(SuccessUrlOrderMixin, DeleteView):
    model = Order
    template_name = "storeapp/Order/Order_Delete.html"
    success_url = reverse_lazy("storeapp:order_list")


class HomeView(TemplateView):
    template_name = "storeapp/Additional/Home.html"
    succes_url = reverse_lazy('storeapp:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:10]
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Отримуємо ID продукту з URL
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Знаходимо або створюємо кошик (Order зі статусом 'incart')
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="incart"
        )

        # Знаходимо або створюємо запис про товар у цьому замовленні
        order_product, created = Order_product.objects.get_or_create(
            order=order,
            product=product,
            defaults={'amount': 1}
        )

        # Якщо товар вже був у кошику — збільшуємо кількість
        if not created:
            order_product.amount += 1
            order_product.save()

        # Повертаємо користувача на сторінку, з якої він прийшов, або в кошик
        return redirect(request.META.get('HTTP_REFERER', 'storeapp:product_list'))


class CartView(LoginRequiredMixin, ListView):
    model = Order_product
    template_name = "storeapp/Additional/Cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        # Фільтруємо товари в кошику саме для поточного юзера
        return Order_product.objects.filter(
            order__user=self.request.user,
            order__status="incart"
        )

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "storeapp/Additional/Profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо всі замовлення користувача, крім поточного кошика
        context['orders'] = Order.objects.filter(
            user=self.request.user
        ).exclude(status='incart')
        return context


class AboutView(TemplateView):
    template_name = "storeapp/Additional/About.html"
    succes_url = reverse_lazy('storeapp:about')


class CustomLoginView(LoginView):
    template_name = "storeapp/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "storeapp:login"


class RegisterView(CreateView):
    template_name = "storeapp/Additional/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("storeapp:login"))
