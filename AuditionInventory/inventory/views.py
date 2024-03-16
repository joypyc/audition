from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Supplier
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductUpdateView(APIView):
    def patch(self, request):
        try:
            request_data = request.POST
            record_id = request_data['id']
            product = Product.objects.get(id=record_id)
            for field in request_data:
                values = request_data.get(field)
                setattr(product, field, values)
            product.save()
            return JsonResponse({}, status=200)
        except Product.DoesNotExist as e:
            return JsonResponse({"error": "Record does not exist"}, status=404)


class ProductFilterView(APIView):
    def get(self, request):
        filters = {}
        categories = Category.objects.all().values('id', 'name')
        suppliers = Supplier.objects.all().values('id', 'name')
        filters['category'] = [
            {
                "id": category['id'],
                "label": category['name']
            }
            for category in categories]
        filters['supplier'] = [
            {"id": supplier['id'],
             "label": supplier['name']
             }
            for supplier in suppliers]
        return JsonResponse(filters, status=200)


class DynamicPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100  # Set a maximum page size if needed


class ProductDatatableView(APIView):
    pagination_class = DynamicPagination

    def get(self, request):
        queryset = Product.objects.all().order_by('-id')

        # Filter by category
        categories = request.GET.getlist('category')
        if categories:
            queryset = queryset.filter(product_category__id__in=categories)

        # Filter by supplier
        suppliers = request.GET.getlist('supplier')
        if suppliers:
            queryset = queryset.filter(product_supplier__id__in=suppliers)

        # Search by name (case-insensitive partial match)
        search_term = request.GET.get('searchTerm', None)
        if search_term:
            queryset = queryset.filter(Q(name__icontains=search_term)|Q(product_category__name__icontains=search_term)|
                                       Q(product_supplier__name__icontains=search_term)|Q(id__icontains=search_term)|
                                       Q(price__icontains=search_term)|Q(quantity__icontains=search_term)
                                       )
        total_records_count = queryset.count()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize paginated queryset
        serializer = ProductSerializer(paginated_queryset, many=True)
        # Get the total number of items
        total_items = queryset.count()

        # Calculate the total number of pages
        total_pages = (total_items + paginator.page_size - 1) // paginator.page_size

        current_page = paginator.page.number

        # Generate next page link
        next_page_link = paginator.get_next_link()
        prev_page_link = paginator.get_previous_link()
        return JsonResponse({
            'results': serializer.data,
            'next': next_page_link,
            'previous': prev_page_link,
            'total_pages': total_pages,
            'current_page': current_page,
            "total_records": total_records_count
        })

    def get_next_page_link(self, page_number, page_size):
        current_url = self.request.build_absolute_uri()
        next_page_number = page_number
        next_page_url = f"{current_url}&page={next_page_number}&page_size={page_size}"
        return next_page_url
