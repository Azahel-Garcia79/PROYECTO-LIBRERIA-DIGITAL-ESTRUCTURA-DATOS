from models.libro import Libro
from utils.colores import RESET


class BibliotecaService:
    """Gestiona toda la colección de libros"""
    
    def __init__(self):
        self.primer_libro = None
        self.total_libros = 0
        self.registro_prestamos = []
        self.indice_rapido = {}  # Para búsquedas instantáneas

    # --- OPERACIONES BÁSICAS CON LIBROS ---

    def agregar_libro(self, isbn, titulo, autor, cantidad):
        """Añade un nuevo libro a la biblioteca"""
        from utils.colores import RED, YELLOW, GREEN
        
        if not all([isbn, titulo, autor, cantidad > 0]):
            print(f"{RED} Por favor, completa todos los datos correctamente{RESET}")
            return False

        # Si el libro ya existe, aumentamos la cantidad
        if isbn in self.indice_rapido:
            libro_existente = self.indice_rapido[isbn]
            libro_existente.cantidad += cantidad
            print(f"{YELLOW}📚 Se agregaron {cantidad} copias más de '{titulo}'{RESET}")
            return True

        # Crear nuevo libro
        nuevo_libro = Libro(isbn, titulo, autor, cantidad)
        
        # Agregar a la lista principal
        if self.primer_libro is None:
            self.primer_libro = nuevo_libro
        else:
            actual = self.primer_libro
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_libro
            nuevo_libro.anterior = actual
            
        # Agregar al índice rápido
        self.indice_rapido[isbn] = nuevo_libro
        self.total_libros += 1
        print(f"{GREEN}✨ ¡Nuevo libro agregado: '{titulo}'!{RESET}")
        return True

    def actualizar_libro(self, isbn, nuevos_datos):
        """Actualiza la información de un libro existente"""
        from utils.colores import GREEN, RED
        
        libro = self.indice_rapido.get(isbn)
        if libro:
            if 'titulo' in nuevos_datos:
                libro.titulo = nuevos_datos['titulo']
            if 'autor' in nuevos_datos:
                libro.autor = nuevos_datos['autor']
            if 'cantidad' in nuevos_datos:
                libro.cantidad = nuevos_datos['cantidad']
            print(f"{GREEN} Libro con ISBN {isbn} actualizado{RESET}")
            return True
        else:
            print(f"{RED} No encontramos ningún libro con ese ISBN{RESET}")
            return False

    def eliminar_libro(self, isbn):
        """Elimina un libro de la biblioteca"""
        from utils.colores import GREEN, RED
        
        libro = self.indice_rapido.get(isbn)
        if not libro:
            print(f"{RED} No encontramos ningún libro con ese ISBN{RESET}")
            return False
            
        # Reorganizar los enlaces de la lista
        if libro.anterior is None:
            self.primer_libro = libro.siguiente
        else:
            libro.anterior.siguiente = libro.siguiente
        
        if libro.siguiente:
            libro.siguiente.anterior = libro.anterior
                
        # Eliminar del índice rápido
        del self.indice_rapido[isbn]
        self.total_libros -= 1
        print(f"{GREEN} El libro '{libro.titulo}' fue eliminado{RESET}")
        return True

    # --- MÉTODOS DE BÚSQUEDA ---
    
    def _obtener_libros_ordenados(self, criterio='isbn'):
        """Obtiene todos los libros ordenados por un criterio"""
        from utils.colores import RED
        
        libros = []
        actual = self.primer_libro
        while actual:
            libros.append(actual)
            actual = actual.siguiente
            
        try:
            libros.sort(key=lambda x: getattr(x, criterio))
        except AttributeError:
            print(f"{RED} No podemos ordenar por ese criterio{RESET}")
            return []
        return libros

    def buscar_por_palabra(self, palabra, campo='titulo'):
        """Busca libros que contengan una palabra en título o autor"""
        resultados = []
        actual = self.primer_libro
        while actual:
            if palabra.lower() in str(getattr(actual, campo)).lower():
                resultados.append(actual)
            actual = actual.siguiente
        return resultados

    def buscar_por_isbn_ordenado(self, isbn):
        """Búsqueda rápida en lista ordenada (más eficiente)"""
        libros_ordenados = self._obtener_libros_ordenados('isbn')
        izquierda, derecha = 0, len(libros_ordenados) - 1
        
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            libro_medio = libros_ordenados[medio]
            
            if libro_medio.isbn == isbn:
                return libro_medio
            elif libro_medio.isbn < isbn:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None
        
    def buscar_por_isbn_instantaneo(self, isbn):
        """Búsqueda instantánea usando el índice"""
        return self.indice_rapido.get(isbn)

    # --- PRÉSTAMOS Y DEVOLUCIONES ---

    def prestar_libro(self, isbn):
        """Registra el préstamo de un libro"""
        from utils.colores import GREEN, RED
        
        libro = self.buscar_por_isbn_instantaneo(isbn)
        if not libro:
            print(f"{RED} No encontramos ese libro{RESET}")
            return False
            
        if libro.cantidad > 0:
            libro.cantidad -= 1
            libro.prestados += 1
            self.registro_prestamos.append(f"📖 Prestado: {libro.titulo} ({isbn})")
            print(f"{GREEN} Préstamo exitoso: '{libro.titulo}'. Quedan {libro.cantidad} disponibles{RESET}")
            return True
        else:
            print(f"{RED} Lo sentimos, no hay ejemplares disponibles{RESET}")
            return False

    def devolver_libro(self, isbn):
        """Registra la devolución de un libro"""
        from utils.colores import GREEN, RED
        
        libro = self.buscar_por_isbn_instantaneo(isbn)
        if not libro:
            print(f"{RED} No encontramos ese libro{RESET}")
            return False
            
        if libro.prestados > 0:
            libro.cantidad += 1
            libro.prestados -= 1
            self.registro_prestamos.append(f" Devuelto: {libro.titulo} ({isbn})")
            print(f"{GREEN} ¡Gracias por devolver el libro!{RESET}")
            return True
        else:
            print(f"{RED} Este libro no estaba registrado como prestado{RESET}")
            return False
        
    def limpiar_historial_libro(self, isbn):
        """Elimina el historial de préstamos de un libro específico"""
        from utils.colores import GREEN, YELLOW
        
        cantidad_inicial = len(self.registro_prestamos)
        self.registro_prestamos = [reg for reg in self.registro_prestamos if not f"({isbn})" in reg]
        if len(self.registro_prestamos) < cantidad_inicial:
            print(f"{GREEN} Historial de préstamos limpiado{RESET}")
            return True
        else:
            print(f"{YELLOW}ℹ No había registros para ese libro{RESET}")
            return False
            
    # --- FUNCIÓN RECURSIVA ---

    def _contar_ejemplares_recursivo(self, libro_actual):
        """Cuenta el total de ejemplares usando recursividad"""
        if libro_actual is None:
            return 0
        return libro_actual.cantidad + self._contar_ejemplares_recursivo(libro_actual.siguiente)

    def contar_todos_los_ejemplares(self):
        """Muestra el total de libros disponibles"""
        return self._contar_ejemplares_recursivo(self.primer_libro)
    
    def obtener_todos_libros(self):
        """Devuelve todos los libros para mostrar"""
        libros = []
        actual = self.primer_libro
        while actual:
            libros.append(actual)
            actual = actual.siguiente
        return libros