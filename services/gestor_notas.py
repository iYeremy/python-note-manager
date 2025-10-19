import os
import shutil
import json
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
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except FileNotFoundError:
            return "Nota no encontrada."
        except OSError:
            # El servicio captura errores de E/S para evitar que la interfaz principal se caiga.
            return "No fue posible leer la nota. Intente nuevamente."

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
        if not os.path.exists(ruta):
            return False, "No se encontró la nota."

        respaldo = os.path.join(self.carpeta, f"{nombre}_bak.txt")
        try:
            shutil.copy(ruta, respaldo)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(nuevo_contenido)
            return True, "Nota editada y respaldo creado."
        except OSError:
            # El servicio decide la recuperación porque conoce el contexto de persistencia.
            if os.path.exists(respaldo):
                try:
                    os.remove(respaldo)
                except OSError:
                    pass
            return False, "No fue posible editar la nota. Intente nuevamente más tarde."

    def eliminar(self, nombre):
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if not os.path.exists(ruta):
            return False, "No se encontró la nota."

        try:
            os.remove(ruta)
            return True, "Nota eliminada correctamente."
        except OSError:
            # Propagamos un mensaje genérico para no exponer detalles sensibles al usuario final.
            return False, "No fue posible eliminar la nota. Verifique los permisos e inténtelo más tarde."
    
    def contar(self): # metodo en gestor_notas ya que es el componente que se encarga de la persistencia y gestión de archivos 
        return len([
            a for a in os.listdir(self.carpeta)
            if a.endswith(".txt") and not a.endswith("_bak.txt")
        ])
    
    def exportar_json(self, carpeta_export="exports", archivo_salida="notas.json"):
        """
        Exporta todas las notas almacenadas a un archivo JSON dentro de una subcarpeta.
        Cada nota se representa con: nombre, fecha, contenido.
        """
        carpeta_destino = os.path.join(self.carpeta, carpeta_export)
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        notas = []
        for archivo in os.listdir(self.carpeta):
            if archivo.endswith(".txt") and not archivo.endswith("_bak.txt"):
                ruta = os.path.join(self.carpeta, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                nombre = archivo[:-4]
                lineas = contenido.splitlines()
                fecha = lineas[0].replace("Fecha: ", "").strip() if lineas else ""
                cuerpo = "\n".join(lineas[2:]) if len(lineas) > 2 else ""
                notas.append({
                    "nombre": nombre,
                    "fecha": fecha,
                    "contenido": cuerpo
                })

        ruta_json = os.path.join(carpeta_destino, archivo_salida)
        with open(ruta_json, "w", encoding="utf-8") as json_file:
            json.dump(notas, json_file, indent=4, ensure_ascii=False)

        return True
