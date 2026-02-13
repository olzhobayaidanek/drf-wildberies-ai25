from .models import Product,Category,Subcategory
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)











