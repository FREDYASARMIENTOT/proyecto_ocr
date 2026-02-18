import cv2
import pytesseract
import os

import pytesseract

import os
import pytesseract

# 1. Definimos la ruta base del motor
ruta_base = r'C:\Program Files\Tesseract-OCR'

# 2. Configuramos el ejecutable
pytesseract.pytesseract.tesseract_cmd = os.path.join(ruta_base, 'tesseract.exe')

# 3. Configuramos la ruta de los idiomas (TESSDATA) para evitar el error 'spa'
os.environ['TESSDATA_PREFIX'] = os.path.join(ruta_base, 'tessdata')

def preprocesar_imagen(ruta_imagen):
    """Mejora la imagen para el taller (Criterio: Calidad de resultados)"""
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise FileNotFoundError(f"No se encontró la imagen: {ruta_imagen}")
    
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarizada

def ejecutar_ocr(ruta_imagen, lenguaje='spa'):
    """Ejecuta el pipeline (Criterio: Funcionamiento 30%)"""
    try:
        img = preprocesar_imagen(ruta_imagen)
        # IMPORTANTE: No pasamos 'config' con rutas manuales para evitar el error de comillas
        texto = pytesseract.image_to_string(img, lang=lenguaje)
        return texto.strip()
    except Exception as e:
        return f"Error crítico: {str(e)}"