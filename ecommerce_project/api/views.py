from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from products.models import Product, Product_Category
from .serializers import ProductSerializer, ProductCategorySerializer
from .permissions import IsStaffOrReadOnly

# Create your views here.

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "price"]   
    search_fields = ["name", "description"]    
    ordering_fields = ["price", "updated_at"]  
    ordering = ["-updated_at"] 

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ProductCategoryViewset(ModelViewSet):
    serializer_class = ProductCategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    ordering = ["name"]
                          
    def get_queryset(self):
        queryset = Product_Category.objects.prefetch_related('products')
        return queryset