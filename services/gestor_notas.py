import os
import shutil
from models.nota import Nota

class GestorNotas:
    """
    Administra las operaciones de creación, lectura, edición,
    búsqueda y eliminación de notas.
    """

    def __init__(self, carpeta="notas"):
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def guardar(self, nota: Nota):
        ruta = os.path.join(self.carpeta, f"{nota.nombre}.txt")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(str(nota))

    def leer(self, nombre):
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as archivo:
                return archivo.read()
        return "Nota no encontrada."

    def listar(self):
        return [a[:-4] for a in os.listdir(self.carpeta) if a.endswith(".txt")]

    def buscar(self, palabra):
        resultados = []
        for archivo in os.listdir(self.carpeta):
            ruta = os.path.join(self.carpeta, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                if palabra.lower() in f.read().lower():
                    resultados.append(archivo[:-4])
        return resultados

    def editar(self, nombre, nuevo_contenido):
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if os.path.exists(ruta):
            respaldo = os.path.join(self.carpeta, f"{nombre}_bak.txt")
            shutil.copy(ruta, respaldo)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(nuevo_contenido)
            return True
        return False

    def eliminar(self, nombre):
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if os.path.exists(ruta):
            os.remove(ruta)
            return True
        return False
