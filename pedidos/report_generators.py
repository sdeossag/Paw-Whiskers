
from abc import ABC, abstractmethod
from django.http import HttpResponse
import pandas as pd
from .models import Pedido

class ReportGenerator(ABC):
    """
    Interfaz abstracta para definir generadores de reportes.
    """
    @abstractmethod
    def generate(self, pedidos):
        """
        Método abstracto para generar un reporte.
        Debe ser implementado por las clases concretas.
        """
        pass

class ReporteExcelGenerator(ReportGenerator):
    """
    Implementación concreta para generar reportes en formato Excel.
    """
    def generate(self, pedidos):
        # Convertir el queryset de pedidos a un DataFrame de pandas
        data = list(pedidos.values(
            'id', 
            'cliente__username', 
            'fechaPedido', 
            'estado',
            'total'
        ))
        df = pd.DataFrame(data)
        
        # Renombrar columnas para mayor claridad
        df.rename(columns={
            'id': 'ID Pedido',
            'cliente__username': 'Cliente',
            'fechaPedido': 'Fecha',
            'estado': 'Estado',
            'total': 'Total'
        }, inplace=True)

        # Crear una respuesta HTTP con el archivo Excel
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.xlsx"'
        
        # Escribir el DataFrame al response
        df.to_excel(response, index=False)
        
        return response

class ReportePDFGenerator(ReportGenerator):
    """
    Implementación concreta para generar reportes en formato PDF.
    Para este ejemplo, simulamos la creación de un PDF simple.
    """
    def generate(self, pedidos):
        # Crear una respuesta HTTP con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.pdf"'

        # Contenido simple para el PDF (simulación)
        # En un caso real, aquí usaríamos una librería como ReportLab o FPDF
        html = "<h1>Reporte de Pedidos</h1>"
        html += "<table border='1'>"
        html += "<thead><tr><th>ID</th><th>Cliente</th><th>Fecha</th><th>Estado</th><th>Total</th></tr></thead>"
        html += "<tbody>"
        for pedido in pedidos:
            html += f"<tr><td>{pedido.id}</td><td>{pedido.cliente.username}</td><td>{pedido.fechaPedido.strftime('%Y-%m-%d')}</td><td>{pedido.get_estado_display()}</td><td>${pedido.total}</td></tr>"
        html += "</tbody></table>"

        # Aquí podríamos usar una librería para convertir HTML a PDF, 
        # pero por simplicidad, solo escribimos el texto.
        response.write(f"Simulacion de PDF:\n\n{html}".encode('utf-8'))

        return response
