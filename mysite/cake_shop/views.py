from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ProductPagination
from .filters import ProductFilter

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)

class UserListViewSet(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer

class UserDetailViewSet(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer

class BakeryListViewSet(generics.ListAPIView):
    queryset = Bakery.objects.all()
    serializer_class = BakeryListSerializer

class BakeryDetailViewSet(generics.RetrieveAPIView):
    queryset = Bakery.objects.all()
    serializer_class = BakeryDetailSerializer

class CategoryListViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'create_date']
    pagination_class = ProductPagination

class CategoryDetailViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class ProductListViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class OrderListViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

class OrderDetailViewSet(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return CartItem.objects.none()

        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)