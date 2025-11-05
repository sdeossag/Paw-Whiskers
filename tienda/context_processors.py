import requests

def clima_medellin(request):
    """
    Obtiene el clima actual de Medellín desde la API de Open-Meteo.
    """
    try:
        # Coordenadas de Medellín
        latitud = 6.2518
        longitud = -75.5636
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true"

        response = requests.get(url, timeout=5) # Timeout de 5 segundos
        response.raise_for_status()  # Lanza un error para respuestas 4xx/5xx

        data = response.json()
        clima = {
            'temperatura': data['current_weather']['temperature'],
            'codigo_clima': data['current_weather']['weathercode']
        }
        return {'clima_medellin': clima}

    except requests.exceptions.RequestException as e:
        # Si la API falla o hay un error de red, no se mostrará nada.
        print(f"Error al obtener el clima: {e}")
        return {}
    except (KeyError, ValueError) as e:
        # Si la respuesta JSON no tiene el formato esperado.
        print(f"Error al procesar los datos del clima: {e}")
        return {}
