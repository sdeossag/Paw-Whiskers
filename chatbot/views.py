from django.utils.translation import gettext_lazy as _
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .llm import get_llm_instance
from .services import get_context_data

# Inicializar LLM
llm = get_llm_instance()


@csrf_exempt
def chat_view(request):
    """API que responde usando LLM y productos reales"""
    if request.method != "POST":
        return JsonResponse({"error": _("Método no permitido")}, status=405)

    if not llm:
        return JsonResponse({"error": _("Servicio de chatbot no disponible temporalmente")}, status=503)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": _("El mensaje no puede estar vacío")}, status=400)

        # Obtener productos desde la base de datos
        context_data = get_context_data()
        productos_info_text = "\n".join(
            [f"- {p['nombre']} ({p['clasificacion']}): ${p['precio']} - Disponibles: {p['cantidadDisp']}"
             for p in context_data.get("productos", [])]
        ) or _("No hay productos disponibles actualmente.")

        # Construir mensajes para LLM
        messages = [
            {
                "role": "system",
                "content": _(
                    "Eres un asistente especializado en productos para mascotas.\n"
                    "Usa la siguiente información de los productos disponibles para responder al usuario:\n\n"
                    "%(productos)s\n\n"
                    "Si el usuario pregunta algo relacionado con productos, prioriza dar recomendaciones concretas basadas en estos productos.\n"
                    "Si no hay productos relevantes, da consejos generales de mascotas.\n"
                    "Responde de forma clara, amigable y profesional."
                ) % {"productos": productos_info_text},
            },
            {"role": "user", "content": user_message},
        ]

        bot_reply = llm.complete(messages)
        return JsonResponse({"respuesta": bot_reply})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def chatbot_page(request):
    """Renderiza la página del chatbot"""
    return render(request, "chatbot/chatbot.html")
