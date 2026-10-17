from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserListViewSet.as_view(), name='users'),
    path('user/<int:pk>', UserDetailViewSet.as_view(), name='user'),
    path('bakery/', BakeryListViewSet.as_view(), name='bakery'),
    path('bakery/<int:pk>', BakeryDetailViewSet.as_view(), name='bakery_detal'),
    path('category/', CategoryListViewSet.as_view(), name='category'),
    path('category/<int:pk>', CategoryDetailViewSet.as_view(), name='category'),
    path('product/', ProductListViewSet.as_view(), name='product'),
    path('product/<int:pk>', ProductDetailViewSet.as_view(), name='product'),
    path('order/', OrderListViewSet.as_view(), name='order'),
    path('order/<int:pk>', OrderDetailViewSet.as_view(), name='order'),
    path('cart/', CartAPIView.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]