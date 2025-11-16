class Libro:
    """Representa un libro en nuestra colección"""
    def __init__(self, isbn, titulo, autor, cantidad):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.cantidad = cantidad
        self.prestados = 0
        self.siguiente = None
        self.anterior = None

    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"