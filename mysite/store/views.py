from rest_framework import viewsets,generics,permissions,status
from .models import (UserProfile,Category,Subcategory,Product ,
                     ImageProduct,Review,Cart,CartItem,Favorite,FavoriteItem)
from .serializers import (UserProfileSerializers,CategoryListSerializers, CategoryDetailSerializers,
                          SubcategoryListSerializers,SubcategoryDetailSerializers,ProductSerializers,
                          ImageProductSerializers,ReviewSerializers,CartSerializers,CartItemSerializers,
                          FavoriteSerializers,FavoriteItemSerializers,UserSerializer,LoginSerializer)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from.filter import ProductFilter
from .pagination import ProductPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)






class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class CategoryListViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers

class CategoryDetailViewSet(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializers

class SubcategoryListViewSet(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializers

class SubcategoryDetailViewSet(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryDetailSerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price']
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class ImageProductViewSet(viewsets.ModelViewSet):
    queryset = ImageProduct.objects.all()
    serializer_class = ImageProductSerializers

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers




def get_queryset(self):
    return CartItem.objects.filter(cart__user=self.request.user)


def perform_create(self, serializer):
    cart, created = Cart.objects.get_or_create(user=self.request.user)
    serializer.save(cart=cart)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers



    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializers


















