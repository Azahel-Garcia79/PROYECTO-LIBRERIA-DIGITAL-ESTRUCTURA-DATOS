from .colores import RED,RESET

def pausar_para_continuar():
    """Espera que el usuario presione ENTER"""
    from .colores import CYAN, RESET
    input(f"\n{CYAN}Presiona ENTER para continuar...{RESET}")

def obtener_numero_valido(mensaje):
    """Solicita un número válido al usuario"""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print(f"{RED} Por favor, ingresa un número válido{RESET}")

def confirmar_salida():
    """Pide confirmación antes de salir"""
    from .colores import RED, GREEN
    print(f"\n{RED}Atención: Los datos no se guardan automáticamente{RESET}")
    confirmar = input("¿Estás seguro de que quieres salir? [s/N]: ").lower()
    return confirmar == 's'