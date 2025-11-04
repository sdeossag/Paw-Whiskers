from productos.models import Producto

def get_context_data(limit=10):
    """
    Retorna información de los productos activos en la base de datos,
    lista para que el LLM la use en sus respuestas.
    """
    productos = Producto.objects.filter(activo=True)[:limit]
    
    # ✅ Sin traducir - son claves internas del diccionario
    productos_list = [
        {
            "nombre": p.nombre,
            "clasificacion": p.clasificacion,
            "precio": float(p.precio),
            "cantidadDisp": p.cantidadDisp,
        }
        for p in productos
    ]
    
    return {"productos": productos_list}