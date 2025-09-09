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
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "clientes/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f"Bienvenido {username}, tu cuenta fue creada 🎉")
        return redirect("home")

    return render(request, "clientes/register.html")


@user_passes_test(es_admin)
def ver_historial(request):
    actividades_lista = RegistroActividad.objects.all()
    tipos_actividad = RegistroActividad.TIPO_ACTIVIDAD_CHOICES

    # Filtrado
    filtro_tipo = request.GET.get('tipo_actividad', '')
    if filtro_tipo:
        actividades_lista = actividades_lista.filter(tipo_actividad=filtro_tipo)

    # Paginación
    paginator = Paginator(actividades_lista, 15)  # 15 registros por página
    page_number = request.GET.get('page')
    actividades = paginator.get_page(page_number)

    context = {
        'actividades': actividades,
        'tipos_actividad': tipos_actividad,
        'filtro_actual': filtro_tipo
    }
    return render(request, 'clientes/historial.html', context)
