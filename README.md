Pipeline de Extracción de Texto con Visión Artificial (OCR)Maestría en TIC - Aplicaciones de Aprendizaje AutomáticoUniversidad del Rosario1. IntroducciónEste proyecto implementa un sistema de Reconocimiento Óptico de Caracteres (OCR) robusto, diseñado para procesar imágenes con ruido o variaciones de iluminación. El sistema integra un pipeline de preprocesamiento avanzado utilizando la librería OpenCV y el motor de inferencia Tesseract OCR.El objetivo principal es transformar datos no estructurados (imágenes) en texto editable, garantizando alta precisión mediante la binarización adaptativa y la normalización de canales.2. Arquitectura del SistemaEl sistema se divide en tres capas funcionales:Capa de Visión (OpenCV): Encargada del filtrado, conversión a escala de grises y segmentación por umbralización.Motor de Inferencia (Tesseract): Wrapper de Python (pytesseract) que interactúa con el binario de Tesseract OCR para el reconocimiento de patrones.Capa de Interfaz (Inferencia CLI): Punto de entrada del usuario que gestiona argumentos por consola y visualización de resultados.3. Requisitos de Software (Stack Técnico)Para garantizar la reproducibilidad del proyecto, se deben cumplir los siguientes requisitos:Sistema Operativo: Windows 10/11 (Arquitectura de 64 bits recomendada).Lenguaje: Python 3.10 o superior.Librerías Python:opencv-python (Procesamiento de imagen).pytesseract (Wrapper de OCR).Pillow (Manejo de formatos de imagen).Motor Externo: Tesseract OCR v5.0+ (Instalación de 64 bits).4. Guía de Instalación Paso a PasoPaso 1: Clonación del RepositorioPowerShellgit clone https://github.com/FREDYASARMIENTOT/proyecto_ocr.git
cd proyecto_ocr
Paso 2: Instalación del Motor Tesseract (Crucial)Descargar el instalador de 64 bits desde el repositorio oficial de UB-Mannheim.Ejecutar el instalador y asegurar que la ruta de destino sea: C:\Program Files\Tesseract-OCR.Importante: Durante la instalación, desplegar el menú "Additional language data" y marcar Spanish para habilitar el soporte de caracteres especiales (ñ, tildes).Paso 3: Configuración del Entorno Virtual y Dependencias

PowerShell
# Crear entorno virtual
python -m venv venv
# Activar entorno (evite ejecutar con el intérprete de Anaconda/`conda base`)
.\venv\Scripts\activate
# Instalar librerías
pip install -r requirements.txt

> ⚠️ **Nota:** en Windows es fácil terminar usando el intérprete de `conda`
> si éste está configurado como predeterminado. Asegúrese de activar el
> `venv` antes de ejecutar los scripts para evitar errores de rutas y
> versiones de Python discrepantes.
5. Configuración de Variables de Entorno (Windows Fix)Debido a la gestión de rutas en Windows, el script de este proyecto incluye una lógica de "Sanitización de Rutas" para evitar errores de tipo (3221225477).El sistema configura automáticamente el TESSDATA_PREFIX dentro de la ejecución de Python para apuntar a:C:\Program Files\Tesseract-OCR\tessdata6. Lógica del Pipeline OCREl archivo src/ocr_pipeline.py implementa la siguiente secuencia de procesamiento:EtapaTécnicaPropósitoGrayscalecv2.COLOR_BGR2GRAYElimina información cromática innecesaria para reducir carga computacional.Binarizacióncv2.threshold + cv2.THRESH_OTSUSepara el texto del fondo mediante un umbral calculado estadísticamente.Inferenciaimage_to_stringEjecuta el motor Tesseract utilizando el modelo de lenguaje spa.7. Instrucciones de UsoPara procesar una imagen, utilice el script de inferencia proporcionando la ruta relativa del archivo de entrada. A partir de esta versión se incluye un envoltorio en la raíz del proyecto para que no sea necesario cambiar de carpeta:

```powershell
# desde la raíz del repositorio (recomendado)
python inferencia.py --imagen data/nube_uni_bi.jpg

# o bien, especificando la ruta completa al módulo interno
python src/inferencia.py --imagen data/nube_uni_bi.jpg
```

> ⚠️ **Importante:** no intente ejecutar `src/ocr_pipeline.py` directamente. El
> módulo sólo proporciona funciones auxiliares y requiere que las
> dependencias estén instaladas en el entorno activo, de lo contrario verá
> errores tipo `ModuleNotFoundError` (por ejemplo si está usando el intérprete
> de Anaconda/`conda base`). Siempre arranque el CLI a través de
> `inferencia.py` con el entorno virtual activado.

8. Solución de Problemas (Troubleshooting)Error: Failed loading language 'spa'Causa: El archivo spa.traineddata no se encuentra en la subcarpeta tessdata.Solución: Descargar el archivo manualmente desde el repositorio oficial de Tesseract y pegarlo en C:\Program Files\Tesseract-OCR\tessdata.Error: (3221225477) o Violación de AccesoCausa: Conflicto entre arquitecturas (Python 64-bit vs Tesseract 32-bit).Solución: Desinstalar cualquier versión de Tesseract de C:\Program Files (x86) e instalar únicamente la de 64-bit en C:\Program Files.9. Estructura del ProyectoPlaintextproyecto_ocr/
├── data/               # Imágenes de prueba (.jpg, .png)
├── src/                # Código fuente del sistema
│   ├── ocr_pipeline.py # Lógica de procesamiento y configuración
│   └── inferencia.py   # Script de ejecución por consola
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación técnica
Autores:  Jorge Bravo, Manuel Caro, Fredy Alejandro Sarmiento Torres