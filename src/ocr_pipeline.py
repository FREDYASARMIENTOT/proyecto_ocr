import cv2
import pytesseract
import os
import logging
import numpy as np
from typing import Optional

# Configuración de logs para trazabilidad profesional
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [Pipeline OCR] - %(message)s'
)

# Configuración de rutas del motor Tesseract (Windows)
ruta_base = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = os.path.join(ruta_base, 'tesseract.exe')
os.environ['TESSDATA_PREFIX'] = os.path.join(ruta_base, 'tessdata')

def verificar_motor() -> bool:
    """Valida la integridad y existencia del binario de Tesseract antes de la ejecución."""
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        logging.error(f"Binario crítico no encontrado en: {ruta_base}")
        return False
    return True

def preprocesar_imagen(ruta_imagen: str) -> np.ndarray:
    """
    Aplica una secuencia de técnicas de Visión Artificial para maximizar la legibilidad:
    1. Conversión a escala de grises.
    2. Suavizado gaussiano para atenuar ruido de alta frecuencia.
    3. Binarización Global de Otsu.
    """
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise FileNotFoundError(f"La matriz de imagen no pudo ser cargada desde: {ruta_imagen}")
    
    # 1. Eliminación de información cromática (Grayscale)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # 2. Reducción de ruido espacial (Filtro Gaussiano 5x5)
    # Vital para evitar que imperfecciones del fondo afecten el cálculo de varianza de Otsu
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    
    # 3. Binarización Adaptativa (Otsu)
    _, binarizada = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    logging.info(f"Fase de preprocesamiento completada para: {os.path.basename(ruta_imagen)}")
    return binarizada

def ejecutar_ocr(ruta_imagen: str, lenguaje: str = 'spa') -> str:
    """
    Orquesta el pipeline completo: desde la carga de la imagen hasta la inferencia de texto.
    """
    if not verificar_motor():
        raise EnvironmentError("El sistema no cuenta con las dependencias del motor OCR.")

    try:
        # Etapa 1: Visión Artificial
        img_procesada = preprocesar_imagen(ruta_imagen)
        
        # Etapa 2: Inferencia de Patrones
        # OEM 3: Default, PSM 3: Fully automatic page segmentation
        config_custom = r'--oem 3 --psm 3'
        
        texto = pytesseract.image_to_string(img_procesada, lang=lenguaje, config=config_custom)
        
        if not texto.strip():
            logging.warning("La inferencia finalizó, pero no se detectaron caracteres estructurados.")
            
        logging.info("Extracción de texto ejecutada exitosamente.")
        return texto.strip()
        
    except Exception as e:
        logging.error(f"Excepción controlada durante la inferencia: {str(e)}")
        raise RuntimeError(f"Fallo en el pipeline de procesamiento: {str(e)}")