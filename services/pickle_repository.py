import os
import pickle


class PickleRepository:
    """
    Encapsula la persistencia binaria de las notas.

    Ventajas: un solo archivo serializa el estado completo, el acceso es rápido
    y reutiliza la serialización nativa de Python. Limitaciones: el formato no
    es legible por humanos, no es seguro cargar datos de fuentes no confiables y
    depende de la versión de Python/pickle.
    """

    def __init__(self, ruta_archivo="notas.pkl"):
        self.ruta_archivo = ruta_archivo

    def guardar(self, datos):
        """Escribe el diccionario de notas serializado en disco."""
        carpeta_destino = os.path.dirname(self.ruta_archivo)
        if carpeta_destino and not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        try:
            with open(self.ruta_archivo, "wb") as archivo:
                pickle.dump(datos, archivo)
        except (OSError, pickle.PickleError):
            return False
        return True

    def cargar(self):
        """Recupera el diccionario de notas desde el archivo binario."""
        if not os.path.exists(self.ruta_archivo):
            return {}
        try:
            with open(self.ruta_archivo, "rb") as archivo:
                datos = pickle.load(archivo)
        except (OSError, pickle.PickleError):
            return {}

        if not isinstance(datos, dict):
            return {}
        return datos
