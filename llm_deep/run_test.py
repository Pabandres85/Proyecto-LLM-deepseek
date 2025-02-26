"""
Script para ejecutar las pruebas unitarias del proyecto.
"""
import os
import sys
import subprocess

def run_tests():
    """
    Ejecuta las pruebas unitarias con pytest y genera reporte de cobertura.
    """
    print("=== Ejecutando pruebas unitarias ===")
    
    # Asegurarnos de que exista el directorio de pruebas
    if not os.path.exists("tests"):
        print("Error: No se encontró el directorio 'tests'.")
        return False
    
    # Comando para ejecutar pruebas con generación de reporte de cobertura
    cmd = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v",
        "--cov=utils", "--cov=services", "--cov=models",
        "--cov-report=term", "--cov-report=html:coverage_html"
    ]
    
    try:
        # Ejecutar el comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Mostrar la salida
        print(result.stdout)
        
        if result.stderr:
            print("Errores:")
            print(result.stderr)
        
        # Verificar si las pruebas pasaron
        if result.returncode == 0:
            print("\n✅ Todas las pruebas pasaron con éxito!")
            print("\nPuedes ver el reporte detallado de cobertura en el directorio 'coverage_html'.")
            return True
        else:
            print("\n❌ Algunas pruebas fallaron.")
            return False
            
    except Exception as e:
        print(f"Error al ejecutar las pruebas: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)