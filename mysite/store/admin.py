from django.contrib import admin
from .models import (UserProfile,Category,Subcategory,Product,
                     ImageProduct,Review,Cart,CartItem,Favorite,FavoriteItem)

from modeltranslation.admin import TranslationAdmin

class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    extra = 1


@admin.register(Category,Subcategory)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Product)
class AllAdmin(TranslationAdmin):
    inlines = [ImageProductInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }







admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)




