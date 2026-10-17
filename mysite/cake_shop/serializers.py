from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password', 'phone_number', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = UserProfile(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})



        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =  ['id', 'username', 'email', 'first_name', 'last_name']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'last_login', 'first_name', 'is_active', 'date_joined', 'name', 'last_name', 'age', 'avatar', 'email', 'country', 'city']

class BakeryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery
        fields = ['id', 'name', 'country', 'city', 'image']

class BakeryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery
        fields = ['id', 'name', 'country', 'address', 'city', 'image', 'user']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class ProductForCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'has']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductForCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'description', 'products']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductForOrderSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'price', 'images']

class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'price', 'has']

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'price', 'has', 'description', 'kg', 'user', 'category']

class OrderListSerializer(serializers.ModelSerializer):
    product = ProductForOrderSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'role', 'quantity', 'product']

class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductForOrderSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'role', 'quantity', 'product', 'date_order', 'date_complete', 'client']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()