from django.urls import path
from .views import chatbot_page, chat_view

urlpatterns = [
    path("", chatbot_page, name="chatbot_page"),  # Página principal del chatbot
    path("ask/", chat_view, name="chat_view"),   # API para chat general

]