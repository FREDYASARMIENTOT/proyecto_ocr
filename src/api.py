from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from .ocr_pipeline import ejecutar_ocr

# Configuración de la aplicación con metadatos profesionales
app = FastAPI(
    title="OCR API - Universidad del Rosario",
    description="Servicio de extracción de texto mediante visión artificial y binarización de Otsu.",
    version="2.0.0",
    contact={
        "name": "Equipo: Bravo, Caro, Sarmiento",
        "url": "https://github.com/FREDYASARMIENTOT/proyecto_ocr",
    }
)

# Carpeta temporal para procesar las imágenes subidas
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ocr", 
          summary="Procesar imagen y extraer texto",
          description="Sube una imagen (JPG, PNG) para procesarla con el pipeline de OpenCV y Tesseract.")
async def ocr_endpoint(file: UploadFile = File(...)):
    # 1. Validación de tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail=f"Archivo no válido: '{file.content_type}'. Se requiere una imagen."
        )

    # 2. Generación de ruta temporal con identificador único
    file_extension = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        # 3. Almacenamiento temporal de la imagen
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 4. Ejecución del pipeline de OCR (OpenCV + Tesseract)
        texto_extraido = ejecutar_ocr(file_path)

        # 5. Respuesta JSON estructurada y profesional
        return {
            "metadata": {
                "filename": file.filename,
                "status": "success",
                "processed_at": uuid.uuid1()
            },
            "analysis": {
                "engine": "Tesseract OCR v5.0",
                "preprocessing": "OpenCV Binarization (Otsu Threshold)",
                "language_detected": "spa",
                "word_count": len(texto_extraido.split())
            },
            "data": {
                "extracted_text": texto_extraido.strip()
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Fallo en el procesamiento: {str(e)}",
                "context": "Maestría ICT - Aplicaciones Aprendizaje Automático"
            }
        )
    
    finally:
        # 6. Limpieza garantizada del archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/", include_in_schema=False)
async def root():
    """Redireccionamiento informativo a la documentación."""
    return {
        "proyecto": "Pipeline de OCR con Visión Artificial",
        "institucion": "Universidad del Rosario",
        "docs": "/docs"
    }