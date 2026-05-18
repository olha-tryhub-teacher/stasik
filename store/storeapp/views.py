import random
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

        categories_map = {
            "Письмове приладдя": ["ручк", "олівец", "рука", "pen", "pencil"],
            "Маркери та виділювачі": ["маркер", "виділювач", "marker", "textmarker", "хайлайтер"],
            "Паперова продукція": ["папір", "зошит", "блокнот", "щоденник", "paper", "notebook"],
            "Офісне приладдя": ["степлер", "ножиц", "дірокол", "скріпк", "клей", "гумка", "стругач"]
        }

        created_categories = {}
        for cat_name in categories_map.keys():
            cat, created = Category.objects.get_or_create(title=cat_name)
            created_categories[cat_name] = cat


        default_cat, created = Category.objects.get_or_create(title="Інші товари")


        all_products = Product.objects.all()
        for prod in all_products:
            title_lower = prod.title.lower() if prod.title else ""
            assigned = False


            for cat_name, keywords in categories_map.items():
                if any(keyword in title_lower for keyword in keywords):
                    prod.category = created_categories[cat_name]
                    prod.save()
                    assigned = True
                    break


            if not assigned:
                if prod.id == 2 or "набір" in title_lower:

                    prod.category = created_categories["Маркери та виділювачі"]
                else:
                    prod.category = created_categories["Письмове приладдя"]
                prod.save()


        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.annotate(prod_count=Count('product')).filter(prod_count__gt=0)
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
    template_name = "storeapp/Product/Product_Create.html"
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
    template_name = "storeapp/Category/Category_List.html"
    success_url = reverse_lazy("storeapp:category_list")


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = "storeapp/Manufacturer/Manufacturer_List.html"
    context_object_name = "manufacturers"


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = "storeapp/Manufacturer/Manufacturer_Detail.html"
    context_object_name = "manufacturer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(manufacturer=self.object)
        return context


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


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "storeapp/Order/Order_List.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).exclude(status='incart').order_by('-id')


class OrderDetailView(DetailView):
    model = Order
    template_name = "storeapp/Order/Order_Detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Order_product.objects.filter(order=self.object)
        return context


class SecretView(LoginRequiredMixin, TemplateView):
    template_name = "storeapp/Additional/secret.html"


class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status="incart").first()
        if order:
            order.status = "pending"
            order.save()
        return redirect('storeapp:order_list')


class OrderUpdateView(CreateUpdateMixin, SuccessUrlOrderMixin, UpdateView):
    model = Order
    fields = "__all__"
    template_name = "storeapp/Order/Order_Update.html"
    success_url = reverse_lazy("storeapp:order_list")


class OrderDeleteView(SuccessUrlOrderMixin, DeleteView):
    model = Order
    template_name = "storeapp/Order/Order_Delete.html"
    success_url = reverse_lazy("storeapp:order_list")


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, id=pk, user=request.user)
        order.delete()
        return redirect('storeapp:order_list')


class HomeView(TemplateView):
    template_name = "storeapp/Additional/Home.html"
    succes_url = reverse_lazy('storeapp:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:10]
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        order, created = Order.objects.get_or_create(user=request.user, status="incart")
        order_product, created = Order_product.objects.get_or_create(
            order=order, product=product, defaults={'amount': quantity}
        )

        if not created:
            order_product.amount = quantity
        order_product.save()

        return redirect('storeapp:cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(
            Order_product, id=item_id, order__user=request.user, order__status="incart"
        )
        cart_item.delete()
        return redirect('storeapp:cart')


class CartView(LoginRequiredMixin, ListView):
    model = Order_product
    template_name = "storeapp/Additional/Cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return Order_product.objects.filter(order__user=self.request.user, order__status="incart")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        context['total_sum'] = sum(item.get_total_price() for item in cart_items)
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "storeapp/Additional/Profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        orders = Order.objects.filter(user=user).exclude(status='incart').order_by('-id')
        context['orders'] = orders

        context['total_orders_count'] = orders.count()

        context['total_spent'] = sum(order.get_total_price() for order in orders)

        cart_products = Order_product.objects.filter(order__user=user, order__status="incart")
        context['cart_items_count'] = sum(item.amount for item in cart_products)

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


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status="incart").first()
        if order:
            order.status = "pending"
            order.save()
        return redirect('storeapp:order_list')