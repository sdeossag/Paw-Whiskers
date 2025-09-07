from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "clasificacion", "precio", "cantidadDisp", "imagen"]

    # Validar que no se repitan productos por nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if Producto.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un producto con este nombre.")
        return nombre
