from django.urls import path,include
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from rest_framework import routers
from .views import (UserProfileViewSet, CategoryListViewSet, CategoryDetailViewSet, SubcategoryListSerializers,
                    SubcategoryDetailSerializers, ProductViewSet,
                    ImageProductViewSet, ReviewViewSet, CartViewSet, CartItemViewSet,
                    FavoriteViewSet, FavoriteItemViewSet, SubcategoryListViewSet, SubcategoryDetailViewSet,
                    RegisterView, CustomLoginView, LogoutView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




router = routers.DefaultRouter()

router.register(r'user_profile',UserProfileViewSet,basename='user-profile')
router.register(r'product',ProductViewSet,basename='product')
router.register(r'image_product',ImageProductViewSet,basename='image-product')
router.register(r'review',ReviewViewSet,basename='review')

urlpatterns = [
    path('',include(router.urls)),

    path('register/',RegisterView.as_view(),name='register_list'),
    path('login/',CustomLoginView.as_view(),name='login_list'),
    path('logout/', LogoutView.as_view(),name='logout_list'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('category/',CategoryListViewSet.as_view(),name='category-list'),
    path('category/<int:pk>/', CategoryDetailViewSet.as_view(),name='category-detail'),

    path('subcategory/', SubcategoryListViewSet.as_view(),name='subcategory-list'),
    path('subcategory/<int:pk>/',SubcategoryDetailViewSet.as_view(),name='subcategory-detail'),

    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_detail'),

    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart_item_list'),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

    path('favorite/', FavoriteViewSet.as_view({'get': 'retrieve'}), name='favorite_detail'),

    path('favorite_items/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_list'),
    path('favorite_items/<int:pk>/', FavoriteItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]

