import os
import shutil
import json
from datetime import datetime
from models.nota import Nota

class GestorNotas:
    """Gestiona la creación, consulta y administración de notas en disco."""

    def __init__(self, carpeta="notas"):
        """Inicializa el directorio de trabajo para almacenar las notas."""
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def guardar(self, nota: Nota):
        """Escribe una nota nueva o reemplaza la existente con el mismo nombre."""
        ruta = os.path.join(self.carpeta, f"{nota.nombre}.txt")
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(str(nota))
        except OSError:
            # Contener errores de escritura mantiene estable a la capa de interfaz.
            return False, "No fue posible guardar la nota. Verifique permisos y reintente."
        return True, "Nota guardada correctamente."

    def leer(self, nombre):
        """Obtiene el contenido de una nota por nombre y maneja fallos de lectura."""
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
        """Devuelve los nombres de todas las notas disponibles en el directorio."""
        try:
            notas = [
                a[:-4]
                for a in os.listdir(self.carpeta)
                if a.endswith(".txt") and not a.endswith("_bak.txt")
            ]
            return True, notas
        except OSError:
            return False, "No fue posible listar las notas. Intente nuevamente."

    def buscar(self, palabra):
        """Busca una palabra en todas las notas y lista las coincidencias por nombre."""
        resultados = []
        for archivo in os.listdir(self.carpeta):
            ruta = os.path.join(self.carpeta, archivo)
            if not archivo.endswith(".txt") or archivo.endswith("_bak.txt"):
                continue
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    if palabra.lower() in f.read().lower():
                        resultados.append(archivo[:-4])
            except OSError:
                # Se ignoran errores de E/S individuales para continuar con la búsqueda global.
                continue
        return resultados

    def editar(self, nombre, nuevo_contenido):
        """Reemplaza el contenido de una nota y conserva una copia de respaldo."""
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if not os.path.exists(ruta):
            return False, "No se encontró la nota."

        respaldo = os.path.join(self.carpeta, f"{nombre}_bak.txt")
        try:
            with open(ruta, "r", encoding="utf-8") as archivo_original:
                contenido_original = archivo_original.read()
        except OSError:
            return False, "No fue posible editar la nota. Intente nuevamente más tarde."

        lineas = contenido_original.splitlines()
        encabezado = lineas[0] if lineas else f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if not encabezado.startswith("Fecha: "):
            encabezado = f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        cuerpo = nuevo_contenido.strip()

        try:
            shutil.copy(ruta, respaldo)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(f"{encabezado}\n\n{cuerpo}" if cuerpo else f"{encabezado}\n\n")
            return True, "Nota editada y respaldo creado."
        except OSError:
            # El servicio decide la recuperación porque conoce el contexto de persistencia.
            restaurado = False
            if os.path.exists(respaldo):
                try:
                    shutil.copy(respaldo, ruta)
                    restaurado = True
                except OSError:
                    pass
            if not restaurado:
                return (
                    False,
                    "No fue posible editar la nota y el contenido anterior quedó resguardado en el respaldo.",
                )
            return False, "No fue posible editar la nota. El contenido original fue restaurado."

    def eliminar(self, nombre):
        """Elimina una nota por nombre y responde con mensajes seguros."""
        ruta = os.path.join(self.carpeta, f"{nombre}.txt")
        if not os.path.exists(ruta):
            return False, "No se encontró la nota."

        try:
            os.remove(ruta)
            return True, "Nota eliminada correctamente."
        except OSError:
            # Propagamos un mensaje genérico para no exponer detalles sensibles al usuario final.
            return False, "No fue posible eliminar la nota. Verifique los permisos e inténtelo más tarde."
    
    def contar(self):
        """Cuenta notas válidas, excluyendo los respaldos de edición."""
        return len([
            a for a in os.listdir(self.carpeta)
            if a.endswith(".txt") and not a.endswith("_bak.txt")
        ])
    
    def exportar_json(self, carpeta_export="exports", archivo_salida="notas.json"):
        """Genera un archivo JSON con todas las notas y sus metadatos básicos."""
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
