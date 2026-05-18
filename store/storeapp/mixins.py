from django.urls import reverse_lazy
from django.shortcuts import redirect

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('storeapp:home')
        return super().dispatch(request, *args, **kwargs)

class CreateUpdateMixin:
    fields = "__all__"

class SuccessUrlProductMixin:
    success_url = reverse_lazy("storeapp:product_list")

class SuccessUrlCategoryMixin:
    success_url = reverse_lazy("storeapp:category_list")

class SuccessUrlManufacturerMixin:
    success_url = reverse_lazy("storeapp:manufacturer_list")

class SuccessUrlOrderMixin:
    success_url = reverse_lazy("storeapp:order_list")

