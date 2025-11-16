#!/usr/bin/env python3
"""
BIBLIOTECA DIGITAL - Sistema de Gestión de Libros
Autor: Tu Nombre
Descripción: Sistema completo de gestión bibliotecaria con múltiples métodos de búsqueda
"""

import sys
import os

# Agregar las carpetas al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), 'modelos'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'servicios'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from ui.interfaz import InterfazBiblioteca

def main():
    """Función principal que inicia la aplicación"""
    try:
        app = InterfazBiblioteca()
        app.ejecutar()
    except KeyboardInterrupt:
        print(f"\n\n¡Hasta pronto! 👋")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()