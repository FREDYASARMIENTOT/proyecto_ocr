import os
import sys
import argparse

# Configuración de rutas: aseguramos que el directorio 'src' sea visible
# Esto permite importar módulos internos sin conflictos de ubicación.
root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # Importación del pipeline de procesamiento
    from ocr_pipeline import ejecutar_ocr
except ImportError as e:
    print(f"Error: No se pudo encontrar el módulo 'ocr_pipeline' en la carpeta 'src'.")
    print(f"Detalle: {e}")
    sys.exit(1)

def main():
    """
    Función principal para la ejecución por línea de comandos (CLI).
    """
    parser = argparse.ArgumentParser(
        description="Sistema de Extracción de Texto (OCR) mediante Visión Artificial."
    )
    
    # Definición de argumentos de consola
    parser.add_argument(
        "--imagen", 
        required=True, 
        help="Ruta de la imagen a procesar (ejemplo: data/nube_uni_bi.jpg)"
    )
    
    args = parser.parse_args()

    # Validación de la existencia de la imagen antes de procesar
    if not os.path.exists(args.imagen):
        print(f"Error: El archivo '{args.imagen}' no existe.")
        return

    print(f"\n[Procesando]: {os.path.basename(args.imagen)}")
    print("=" * 40)
    
    try:
        # Llamada al motor de procesamiento y OCR
        texto_resultado = ejecutar_ocr(args.imagen)
        
        if texto_resultado:
            print("Resultado de la extracción:")
            print("-" * 40)
            print(texto_resultado)
        else:
            print("Aviso: No se pudo extraer texto de la imagen.")
            
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    
    print("=" * 40)

if __name__ == "__main__":
    main()