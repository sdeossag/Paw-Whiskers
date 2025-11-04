from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import RegistroActividad
from django.core.paginator import Paginator

def es_admin(user):
    return user.is_superuser

def login_view(request):
    if request.method == "POST":  # ❌ NO traducir "POST"
        username = request.POST.get("username")  # ❌ NO traducir "username"
        password = request.POST.get("password")  # ❌ NO traducir "password"
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, _("Usuario o contraseña incorrectos"))  # ✅ SÍ traducir mensajes
    
    return render(request, "clientes/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.method == "POST":  # ❌ NO traducir "POST"
        username = request.POST.get("username")  # ❌ NO traducir nombres de campos
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, _("Las contraseñas no coinciden"))  # ✅ SÍ traducir mensajes
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, _("El usuario ya existe"))  # ✅ SÍ traducir mensajes
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, _("Bienvenido %(username)s, tu cuenta fue creada 🎉") % {'username': username})  # ✅ SÍ traducir mensajes
        return redirect("home")

    return render(request, "clientes/register.html")


@user_passes_test(es_admin)
def ver_historial(request):
    actividades_lista = RegistroActividad.objects.all()
    tipos_actividad = RegistroActividad.TIPO_ACTIVIDAD_CHOICES

    # Filtrado
    filtro_tipo = request.GET.get("tipo_actividad", '')  # ❌ NO traducir nombres de parámetros
    if filtro_tipo:
        actividades_lista = actividades_lista.filter(tipo_actividad=filtro_tipo)

    # Paginación
    paginator = Paginator(actividades_lista, 15)  # 15 registros por página
    page_number = request.GET.get("page")  # ❌ NO traducir "page"
    actividades = paginator.get_page(page_number)

    context = {
        "actividades": actividades,  # ❌ NO traducir nombres de variables en contexto
        "tipos_actividad": tipos_actividad,
        "filtro_actual": filtro_tipo
    }
    return render(request, 'clientes/historial.html', context)