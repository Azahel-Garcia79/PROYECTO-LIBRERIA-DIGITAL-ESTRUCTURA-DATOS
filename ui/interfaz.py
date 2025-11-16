from services.biblioteca_service import BibliotecaService
from ui.menus import mostrar_menu_principal, menu_gestion_libros, menu_busquedas, menu_prestamos
from utils.helpers import confirmar_salida
from utils.colores import GREEN, RED,RESET

class InterfazBiblioteca:
    """Controla la interfaz de usuario de la biblioteca"""
    
    def __init__(self):
        self.biblioteca_service = BibliotecaService()
    
    def ejecutar(self):
        """Inicia la aplicación de la biblioteca"""
        print(f"{GREEN}¡Bienvenido a la Biblioteca Digital!{RESET}")
        
        while True:
            opcion = mostrar_menu_principal()
            
            if opcion == '1':
                menu_gestion_libros(self.biblioteca_service)
            elif opcion == '2':
                menu_busquedas(self.biblioteca_service)
            elif opcion == '3':
                menu_prestamos(self.biblioteca_service)
            
            # Opción para salir
            elif opcion == '4':
                if confirmar_salida():
                    print(f"\n{GREEN}¡Gracias por usar la Biblioteca Digital! ¡Hasta pronto! 👋{RESET}")
                    return
            else:
                print(f"{RED} Por favor, elige una opción del 1 al 4{RESET}")