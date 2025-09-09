from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),

    # URL para el historial de actividad (solo admin)
    path('historial/', views.ver_historial, name='ver_historial'),
]
