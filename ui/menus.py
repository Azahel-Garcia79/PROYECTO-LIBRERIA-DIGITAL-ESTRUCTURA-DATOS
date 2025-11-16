from utils.colores import CYAN, MAGENTA, RED, GREEN, RESET
from utils.helpers import obtener_numero_valido, pausar_para_continuar

def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "═" * 50)
    print(f"{CYAN}         📚 BIBLIOTECA DIGITAL 📚{RESET}")
    print("═" * 50)
    print(f"{MAGENTA}1. Gestionar Libros (Agregar, Editar, Eliminar){RESET}")
    print(f"{MAGENTA}2. Buscar y Consultar Catálogo{RESET}")
    print(f"{MAGENTA}3. Préstamos y Devoluciones{RESET}")
    print(f"{RED}4. Salir{RESET}")
    print("─" * 50)
    return input("¿Qué te gustaría hacer? [1-4]: ")

def menu_gestion_libros(biblioteca_service):
    """Submenú para gestionar libros"""
    from services.biblioteca_service import BibliotecaService
    
    while True:
        print("\n" + "─" * 40)
        print(f"{CYAN}   GESTIÓN DE LIBROS{RESET}")
        print("─" * 40)
        print(f"{MAGENTA}A. Agregar Nuevo Libro{RESET}")
        print(f"{MAGENTA}B. Actualizar Información{RESET}")
        print(f"{MAGENTA}C. Eliminar Libro{RESET}")
        print(f"{RED}X. Volver al Menú Principal{RESET}")
        
        opcion = input("Elige una opción [A-C, X]: ").upper()
        
        if opcion == 'A':
            print(f"\n{CYAN}➕ AGREGAR NUEVO LIBRO{RESET}")
            isbn = input("ISBN: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            cantidad = obtener_numero_valido("Cantidad de ejemplares: ")
            if cantidad > 0:
                biblioteca_service.agregar_libro(isbn, titulo, autor, cantidad)
                
        elif opcion == 'B':
            print(f"\n{CYAN}✏️ ACTUALIZAR LIBRO{RESET}")
            isbn = input("ISBN del libro a actualizar: ")
            titulo = input("Nuevo título (deja vacío para no cambiar): ")
            autor = input("Nuevo autor (deja vacío para no cambiar): ")
            cantidad_str = input("Nueva cantidad total (deja vacío para no cambiar): ")
            
            nuevos_datos = {}
            if titulo:
                nuevos_datos['titulo'] = titulo
            if autor:
                nuevos_datos['autor'] = autor
            if cantidad_str:
                try:
                    nuevos_datos['cantidad'] = int(cantidad_str)
                except ValueError:
                    print(f"{RED}❌ La cantidad debe ser un número{RESET}")
                    continue
            biblioteca_service.actualizar_libro(isbn, nuevos_datos)

        elif opcion == 'C':
            print(f"\n{CYAN}🗑️ ELIMINAR LIBRO{RESET}")
            biblioteca_service.eliminar_libro(input("ISBN del libro a eliminar: "))
            
        elif opcion == 'X':
            return
        else:
            print(f"{RED}❌ Opción no reconocida{RESET}")
        pausar_para_continuar()

def menu_busquedas(biblioteca_service):
    """Submenú para búsquedas y consultas"""
    from utils.colores import GREEN, YELLOW, CYAN
    
    while True:
        print("\n" + "─" * 40)
        print(f"{CYAN}   BÚSQUEDAS Y CONSULTAS{RESET}")
        print("─" * 40)
        print(f"{MAGENTA}A. Ver Catálogo Completo (Ordenado){RESET}")
        print(f"{MAGENTA}B. Buscar por Título o Autor{RESET}")
        print(f"{MAGENTA}C. Buscar por ISBN (Búsqueda Rápida){RESET}")
        print(f"{MAGENTA}D. Buscar por ISBN (Búsqueda Instantánea){RESET}")
        print(f"{MAGENTA}E. Contar Total de Ejemplares (Recursivo){RESET}")
        print(f"{RED}X. Volver al Menú Principal{RESET}")
        
        opcion = input("Elige una opción [A-E, X]: ").upper()
        
        if opcion == 'A':
            libros_ordenados = biblioteca_service._obtener_libros_ordenados('titulo')
            if not libros_ordenados:
                print(f"{YELLOW}📭 El catálogo está vacío{RESET}")
                pausar_para_continuar()
                continue
                
            print("\n" + "═" * 100)
            print(f"{CYAN}{'ISBN':<15}{'TÍTULO':<35}{'AUTOR':<25}{'DISP.':<8}{'PREST.':<7}{RESET}")
            print("═" * 100)
            for libro in libros_ordenados:
                print(f"{libro.isbn:<15}{libro.titulo:<35}{libro.autor:<25}{libro.cantidad:<8}{libro.prestados:<7}")

        elif opcion == 'B':
            palabra = input("¿Qué libro o autor buscas?: ")
            resultados = biblioteca_service.buscar_por_palabra(palabra)
            if resultados:
                print(f"{GREEN}🎉 Encontramos {len(resultados)} resultados:{RESET}")
                for libro in resultados:
                    print(f"• [{libro.isbn}] {libro.titulo} - {libro.autor} (Disponibles: {libro.cantidad})")
            else:
                print(f"{YELLOW}🔍 No encontramos coincidencias{RESET}")

        elif opcion == 'C':
            isbn = input("Ingresa el ISBN a buscar: ")
            resultado = biblioteca_service.buscar_por_isbn_ordenado(isbn)
            if resultado:
                print(f"{GREEN}✅ Encontrado: {resultado.titulo} ({resultado.cantidad} disponibles){RESET}")
            else:
                print(f"{YELLOW}🔍 ISBN no encontrado{RESET}")
                
        elif opcion == 'D':
            isbn = input("Ingresa el ISBN: ")
            resultado = biblioteca_service.buscar_por_isbn_instantaneo(isbn)
            if resultado:
                print(f"{GREEN}⚡ ¡Encontrado instantáneamente!{RESET}")
                print(f"• Título: {resultado.titulo}")
                print(f"• Disponibles: {resultado.cantidad}")
                print(f"• Prestados: {resultado.prestados}")
            else:
                print(f"{YELLOW}🔍 ISBN no encontrado{RESET}")
        
        elif opcion == 'E':
            total = biblioteca_service.contar_todos_los_ejemplares()
            print(f"{GREEN}📊 Tenemos {total} ejemplares disponibles en total{RESET}")
                
        elif opcion == 'X':
            return
        else:
            print(f"{RED}❌ Opción no válida{RESET}")
        pausar_para_continuar()

def menu_prestamos(biblioteca_service):
    """Submenú para préstamos y devoluciones"""
    from utils.colores import CYAN, MAGENTA, RED, YELLOW, GREEN
    
    while True:
        print("\n" + "─" * 40)
        print(f"{CYAN}   PRÉSTAMOS Y DEVOLUCIONES{RESET}")
        print("─" * 40)
        print(f"{MAGENTA}A. Pedir Libro Prestado{RESET}")
        print(f"{MAGENTA}B. Devolver Libro{RESET}")
        print(f"{MAGENTA}C. Ver Historial de Movimientos{RESET}")
        print(f"{MAGENTA}D. Limpiar Historial de un Libro{RESET}")
        print(f"{RED}X. Volver al Menú Principal{RESET}")
        
        opcion = input("Elige una opción [A-D, X]: ").upper()
        
        if opcion == 'A':
            biblioteca_service.prestar_libro(input("ISBN del libro a prestar: "))
        elif opcion == 'B':
            biblioteca_service.devolver_libro(input("ISBN del libro a devolver: "))
        elif opcion == 'C':
            if biblioteca_service.registro_prestamos:
                print(f"\n{CYAN}📋 HISTORIAL RECIENTE (últimos 10 movimientos){RESET}")
                for i, registro in enumerate(biblioteca_service.registro_prestamos[-10:]):
                    print(f"{i+1}. {registro}")
            else:
                print(f"{YELLOW}📝 Aún no hay movimientos registrados{RESET}")

        elif opcion == 'D':
            biblioteca_service.limpiar_historial_libro(input("ISBN del libro a limpiar: "))
        elif opcion == 'X':
            return
        else:
            print(f"{RED}❌ Opción no válida{RESET}")
        pausar_para_continuar()