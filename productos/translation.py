from modeltranslation.translator import register, TranslationOptions
from .models import Producto

@register(Producto)
class ProductoTranslationOptions(TranslationOptions):
    fields = ('nombre', 'descripcion', 'clasificacion')