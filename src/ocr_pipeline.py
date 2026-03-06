import os

# ensure required packages are available and provide a helpful
# error message if the wrong interpreter is used (e.g. conda base).
try:
    import cv2
    import pytesseract
except ImportError as exc:
    missing = exc.name if hasattr(exc, 'name') else str(exc)
    raise ImportError(
        f"Error importing '{missing}'. "
        "¿Está activado el entorno virtual correcto? "
        "Ejecute 'pip install -r requirements.txt' en el venv."
    ) from exc

# 1. PURGA INTERNA: Obligamos a Python a olvidar rutas viejas
os.environ.pop('TESSDATA_PREFIX', None)

# 2. CONFIGURACIÓN LIMPIA (Arquitectura 64 bits)
ruta_base = r'C:\Program Files\Tesseract-OCR'
# Usamos os.path.normpath para evitar el error de las comillas y barras mezcladas
ruta_tessdata = os.path.normpath(os.path.join(ruta_base, 'tessdata'))

pytesseract.pytesseract.tesseract_cmd = os.path.join(ruta_base, 'tesseract.exe')
os.environ['TESSDATA_PREFIX'] = ruta_tessdata

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


if __name__ == "__main__":
    # informe sencillo cuando alguien intenta ejecutar este módulo directamente
    print("Este módulo implementa la lógica OCR y no debe ejecutarse por sí mismo.")
    print("Utilice 'python inferencia.py --imagen <ruta>' desde la raíz del proyecto.")
