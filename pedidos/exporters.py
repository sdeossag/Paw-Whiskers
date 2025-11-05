"""
Implementación de Inversión de Dependencias (Dependency Inversion Principle)
para la generación de reportes en diferentes formatos.

Patrón: Una interfaz abstracta (ReporteExporter) y dos implementaciones concretas
(CSVExporter y PDFExporter) que pueden ser intercambiadas sin modificar el código cliente.
"""

from abc import ABC, abstractmethod
from django.http import HttpResponse
from django.utils.translation import gettext as _
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


# ============================================================
# INTERFAZ ABSTRACTA (Abstracción de alto nivel)
# ============================================================
class ReporteExporter(ABC):
    """
    Interfaz abstracta que define el contrato para exportar reportes.
    Esta es la abstracción de la que dependen los módulos de alto nivel.
    """
    
    @abstractmethod
    def exportar(self, pedidos):
        """
        Método abstracto que debe ser implementado por las clases concretas.
        
        Args:
            pedidos: QuerySet de pedidos a exportar
            
        Returns:
            HttpResponse con el archivo generado
        """
        pass
    
    @abstractmethod
    def get_content_type(self):
        """Retorna el content type del formato de exportación"""
        pass
    
    @abstractmethod
    def get_file_extension(self):
        """Retorna la extensión del archivo"""
        pass


# ============================================================
# IMPLEMENTACIÓN CONCRETA #1: CSV
# ============================================================
class CSVExporter(ReporteExporter):
    """
    Implementación concreta para exportar reportes en formato CSV.
    """
    
    def get_content_type(self):
        return "text/csv"
    
    def get_file_extension(self):
        return "csv"
    
    def exportar(self, pedidos):
        """
        Exporta los pedidos a formato CSV.
        
        Args:
            pedidos: QuerySet de pedidos
            
        Returns:
            HttpResponse con el archivo CSV
        """
        response = HttpResponse(content_type=self.get_content_type())
        filename = f'reporte_pedidos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{self.get_file_extension()}'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        
        # Escribir encabezados
        writer.writerow([
            _("ID Pedido"),
            _("Cliente"),
            _("Email Cliente"),
            _("Fecha"),
            _("Total"),
            _("Estado"),
            _("Dirección")
        ])

        # Escribir datos de los pedidos
        for pedido in pedidos:
            writer.writerow([
                pedido.id,
                pedido.cliente.user.username,
                pedido.cliente.user.email,
                pedido.fechaPedido,
                f"${pedido.totalPedido}",
                pedido.estado,
                pedido.direccionPedido
            ])

        return response


# ============================================================
# IMPLEMENTACIÓN CONCRETA #2: PDF
# ============================================================
class PDFExporter(ReporteExporter):
    """
    Implementación concreta para exportar reportes en formato PDF.
    Utiliza ReportLab para generar PDFs profesionales.
    """
    
    def get_content_type(self):
        return "application/pdf"
    
    def get_file_extension(self):
        return "pdf"
    
    def exportar(self, pedidos):
        """
        Exporta los pedidos a formato PDF con diseño profesional.
        
        Args:
            pedidos: QuerySet de pedidos
            
        Returns:
            HttpResponse con el archivo PDF
        """
        response = HttpResponse(content_type=self.get_content_type())
        filename = f'reporte_pedidos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{self.get_file_extension()}'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Crear el documento PDF
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Título
        title = Paragraph("Reporte de Pedidos", title_style)
        elements.append(title)
        
        # Fecha de generación
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fecha_text = Paragraph(f"<i>Generado el: {fecha_actual}</i>", styles['Normal'])
        elements.append(fecha_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Crear tabla de datos
        data = [[
            "ID",
            "Cliente",
            "Email",
            "Fecha",
            "Total",
            "Estado"
        ]]
        
        for pedido in pedidos:
            data.append([
                str(pedido.id),
                pedido.cliente.user.username,
                pedido.cliente.user.email,
                pedido.fechaPedido.strftime("%Y-%m-%d"),
                f"${pedido.totalPedido}",
                pedido.estado
            ])
        
        # Crear y estilizar la tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        # Resumen
        elements.append(Spacer(1, 0.3*inch))
        total_pedidos = pedidos.count()
        total_ventas = sum(pedido.totalPedido for pedido in pedidos)
        
        resumen_style = ParagraphStyle(
            'Resumen',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2C3E50'),
        )
        
        resumen = Paragraph(
            f"<b>Resumen:</b> Total de pedidos: {total_pedidos} | "
            f"Ventas totales: ${total_ventas:.2f}",
            resumen_style
        )
        elements.append(resumen)
        
        # Construir el PDF
        doc.build(elements)
        
        return response


# ============================================================
# SERVICIO DE EXPORTACIÓN (Módulo de alto nivel)
# ============================================================
class ReporteService:
    """
    Servicio de alto nivel que utiliza la inversión de dependencias.
    Depende de la abstracción (ReporteExporter), no de implementaciones concretas.
    """
    
    def __init__(self, exporter: ReporteExporter):
        """
        Constructor que recibe una implementación de ReporteExporter.
        
        Args:
            exporter: Instancia de una clase que implementa ReporteExporter
        """
        self.exporter = exporter
    
    def generar_reporte(self, pedidos):
        """
        Genera un reporte utilizando el exportador configurado.
        
        Args:
            pedidos: QuerySet de pedidos a exportar
            
        Returns:
            HttpResponse con el archivo generado
        """
        return self.exporter.exportar(pedidos)