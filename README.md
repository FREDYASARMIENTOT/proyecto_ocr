# Pipeline de Extracción de Texto con Visión Artificial (OCR)
### Maestría en TIC - Aplicaciones de Aprendizaje Automático
**Universidad del Rosario**

---

## 👥 Autores
* **Jorge Bravo**
* **Manuel Caro**
* **Fredy Alejandro Sarmiento Torres**

---

## 1. Introducción
Este proyecto implementa un sistema de Reconocimiento Óptico de Caracteres (OCR) robusto, diseñado para procesar imágenes con ruido, baja resolución o variaciones de iluminación. El sistema integra un pipeline de preprocesamiento avanzado utilizando **OpenCV** y el motor de inferencia **Tesseract OCR v5.0**.

El objetivo principal es transformar datos no estructurados (imágenes) en texto editable, garantizando alta precisión mediante técnicas de segmentación estadística.

---

## 🚀 2. Guía de Evaluación Rápida (Vía Navegador)
Para garantizar la reproducibilidad y evitar errores de rutas en consola, hemos habilitado una interfaz web profesional basada en **FastAPI**. Recomendamos este método para la calificación:

1. **Activar el entorno virtual:** ```powershell
   .\venv\Scripts\activate

   
Lanzar el servidor de la API: ```powershelluvicorn src.api:app --reload --port 8001Acceder a la Interfaz UI: Abra en su navegador: http://127.0.0.1:8001/docsProbar el servicio: Haga clic en POST /ocr -> Try it out -> Cargue una imagen de la carpeta data/ -> Execute.🛠️ 3. Requisitos de Software (Stack Técnico)Sistema Operativo: Windows 10/11 (64 bits).Lenguaje: Python 3.10 o superior.Motor Externo: Tesseract OCR v5.0+ (Instalado en C:\Program Files\Tesseract-OCR).Nota Crítica: Durante la instalación, debe marcar la opción "Additional language data" y seleccionar Spanish para habilitar el soporte de caracteres ñ y tildes.🧠 4. Lógica del Pipeline OCR (Ciencia de Datos)A diferencia de implementaciones básicas, este pipeline utiliza técnicas de procesamiento digital de señales para limpiar la entrada:EtapaTécnicaPropósitoGrayscalecv2.cvtColorElimina la carga computacional del color y resalta el contraste.Gaussian Blurcv2.GaussianBlurSuaviza la imagen (Kernel 5x5) para eliminar el ruido de "sal y pimienta".BinarizaciónOtsu's ThresholdingCalcula el umbral óptimo minimizando la varianza intraclase: $\sigma^2_w(t) = \omega_0(t)\sigma^2_0(t) + \omega_1(t)\sigma^2_1(t)$InferenciaLSTM EngineReconocimiento de patrones mediante redes neuronales recurrentes (Tesseract).📂 5. Estructura del ProyectoPlaintextproyecto_ocr/
├── data/               # Imágenes de prueba (.jpg, .png)
├── src/                # Código fuente del sistema
│   ├── ocr_pipeline.py # Lógica de Visión Artificial (CV2 + Tesseract)
│   └── api.py          # Implementación de FastAPI y Swagger UI
├── inferencia.py       # Wrapper de consola para ejecución desde raíz
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación técnica
🆘 6. Solución de Problemas (Troubleshooting)Error: Failed loading language 'spa': El script configura automáticamente el TESSDATA_PREFIX, pero asegúrese de que el archivo spa.traineddata exista en la subcarpeta tessdata.Error: [WinError 10048]: El puerto 8001 está ocupado. Puede cambiarlo ejecutando el comando uvicorn con --port 8080.Conflicto con Anaconda: Si usa Conda, desactive el entorno base (conda deactivate) antes de activar el venv del proyecto.