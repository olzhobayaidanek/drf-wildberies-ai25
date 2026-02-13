from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import (UserProfile,Category,Subcategory,Product ,
                     ImageProduct,Review,Cart,CartItem,Favorite,FavoriteItem)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializers(serializers.ModelSerializer) :
    class Meta:
        model = UserProfile
        fields = ['id','username','status','user_image','phone_number']

class SubcategoryListSerializers(serializers.ModelSerializer) :
    class Meta:
        model = Subcategory
        fields = ['id','subcategory_name']


class CategoryListSerializers(serializers.ModelSerializer) :


    class Meta:
        model = Category
        fields = ['id','category_name']

class CategoryDetailSerializers(serializers.ModelSerializer) :
    sub_category = SubcategoryListSerializers(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id','category_name','sub_category']


class ImageProductSerializers(serializers.ModelSerializer) :
    class Meta:
        model = ImageProduct
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer) :
    category = CategoryListSerializers()
    sub_category = SubcategoryListSerializers()
    image_product = ImageProductSerializers(read_only=True, many=True)


    class Meta:
        model = Product
        fields = ['id','category','sub_category','product_name',
                  'product_image','price','description','image_product']

class SubcategoryDetailSerializers(serializers.ModelSerializer) :
    sub_products = ProductSerializers(read_only=True, many=True)

    class Meta:
        model = Subcategory
        fields = ['id','subcategory_name','sub_products']


class ReviewSerializers(serializers.ModelSerializer) :
    class Meta:
        model = Review
        fields = '__all__'

class CartItemSimpleSerializers(serializers.ModelSerializer) :
    product = ProductSerializers()
    get_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['quantity','product','get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

class CartItemSerializers(serializers.ModelSerializer) :
    class Meta:
        model = CartItem
        fields = ['id','quantity','product']



class CartSerializers(serializers.ModelSerializer) :
    items = CartItemSimpleSerializers(read_only=True, many=True)
    user = UserProfileSerializers()
    get_all_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','user','items','get_all_total_price']



    def get_all_total_price(self, obj):
        return obj.get_all_total_price()

class FavoriteSerializers(serializers.ModelSerializer) :
    class Meta:
        model = FavoriteItem
        fields = '__all__'

class FavoriteItemSerializers(serializers.ModelSerializer) :
    favorite_items = FavoriteSerializers(read_only=True, many=True)
    user = UserProfileSerializers()

    class Meta:
        model = Favorite
        fields = ['id','user','favorite_items']








