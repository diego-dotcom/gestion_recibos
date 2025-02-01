from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from dotenv import load_dotenv
import os

load_dotenv()

def emitir_pdf(fecha, numero, cliente, direccion, cuit, conceptos):
    """
    Genera un recibo en PDF con múltiples conceptos.
    
    Parámetros:
        fecha (str): Fecha del recibo.
        numero (str): Número del recibo.
        cliente (str): Nombre del cliente.
        direccion (str): Dirección del cliente.
        cuit (str): CUIT del cliente.
        conceptos (list of tuples): Lista de tuplas (concepto, importe).
    """

    # Configuración del PDF y líneas
    w, h = A4
    c = canvas.Canvas(numero + "_" + cliente + ".pdf", pagesize=A4)
    
    xlist = [35, 560]
    ylist = [h - 15, h - 95, h - 175, h - 780, h - 817, h - 827]
    c.grid(xlist, ylist)
    c.line(290, h-15, 290, h-95)
    c.line(470, h-175, 470, h-817)

    # Datos del emisor
    c.setFont("Courier", 12)
    c.drawString(40, h-30, os.getenv("EMISOR_NOMBRE"))
    c.setFont("Courier", 10)
    c.drawString(40, h-45, os.getenv("EMISOR_DIRECCION"))
    c.drawString(40, h-60, os.getenv("EMISOR_CIUDAD"))
    c.drawString(40, h-75, os.getenv("EMISOR_TELEFONO"))
    c.drawString(40, h-90, os.getenv("EMISOR_EMAIL"))

    # Datos del recibo
    c.setFont("Courier", 12)
    c.drawString(300, h-30, "RECIBO DE HONORARIOS")
    c.setFont("Courier", 10)
    c.drawString(400, h-45, (os.getenv("PUNTO_VENTA") + " - " + numero))
    c.drawString(300, h-60, ("Fecha: " + fecha))
    c.drawString(300, h-75, os.getenv("EMISOR_CUIT"))
    c.drawString(300, h-90, "Inicio de actividades: " + os.getenv("EMISOR_INICIO"))

    # Datos del cliente
    c.setFont("Helvetica", 10)
    c.drawString(40, h-115, ("Cliente: " + cliente))
    c.drawString(40, h-135, ("Dirección: " + direccion))
    c.drawString(40, h-155, "IVA: Responsable Monotributo")
    c.drawString(320, h-115, ("CUIT: " + cuit))

    # Cuerpo del recibo con múltiples conceptos
    y_position = h - 200
    total = 0

    for concepto, importe in conceptos:
        c.drawString(40, y_position, concepto)
        c.drawString(510, y_position, f"$ {importe:.2f}")
        total += importe
        y_position -= 20  # Espaciado entre líneas

    # Total del recibo
    c.drawString(40, h-802, "TOTAL:")
    c.drawString(510, h-802, f"$ {total:.2f}")

    # Guardar el PDF
    c.showPage()
    c.save()


# Ejemplo de uso
conceptos = [
    ("Honorarios por servicios prestados", 1000),
    ("Concepto 01", 250),
    ("Concepto 02", 150)
]

