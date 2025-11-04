from django.utils.translation import gettext as _
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [_("nombre"), _("descripcion"), _("clasificacion"), _("precio"), _("cantidadDisp"), _("imagen")]

    # Validar que no se repitan productos por nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get(_("nombre"))
        if Producto.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError(_("Ya existe un producto con este nombre."))
        return nombre