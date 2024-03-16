from django.urls import path

from inventory.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDetailView,ProductDatatableView, ProductFilterView


urlpatterns = [
    path('inventory', ProductDatatableView.as_view()),
    path('inventory/<int:pk>', ProductDetailView.as_view()),
    path('add-inventory', ProductCreateView.as_view()),
    path('update-inventory', ProductUpdateView.as_view()),
    path('delete-inventory', ProductUpdateView.as_view()),
    path('filters', ProductFilterView.as_view())
]