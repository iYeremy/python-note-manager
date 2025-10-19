import json
import os
import tempfile
import unittest
from unittest.mock import patch

from models.nota import Nota
from services.gestor_notas import GestorNotas

# solo testas el servicio de gestor de notas
class GestorNotasTestCase(unittest.TestCase):
    """Pruebas unitarias para el servicio de gestión de notas."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.gestor = GestorNotas(carpeta=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_guardar_y_leer_nota(self):
        nota = Nota("nota_ejemplo", "Contenido de prueba")
        exito, mensaje = self.gestor.guardar(nota)

        self.assertTrue(exito)
        self.assertIn("guardada", mensaje)

        contenido = self.gestor.leer("nota_ejemplo")
        self.assertIn("Contenido de prueba", contenido)

    def test_leer_nota_inexistente(self):
        self.assertEqual(self.gestor.leer("inexistente"), "Nota no encontrada.")

    def test_listar_devuelve_nombres_de_notas(self):
        self.gestor.guardar(Nota("primera", "contenido"))
        self.gestor.guardar(Nota("segunda", "contenido"))

        exito, listado = self.gestor.listar()
        self.assertTrue(exito)
        self.assertCountEqual(listado, ["primera", "segunda"])

    def test_buscar_palabra_en_notas(self):
        self.gestor.guardar(Nota("primera", "un contenido especial"))
        self.gestor.guardar(Nota("segunda", "texto sin coincidencias"))
        os.makedirs(os.path.join(self.temp_dir.name, "exports"))

        coincidencias = self.gestor.buscar("especial")
        self.assertEqual(coincidencias, ["primera"])

    def test_editar_actualiza_contenido_y_crea_respaldo(self):
        self.gestor.guardar(Nota("editable", "texto original"))

        exito, mensaje = self.gestor.editar("editable", "nuevo texto")

        self.assertTrue(exito)
        self.assertIn("editada", mensaje)
        contenido = self.gestor.leer("editable")
        self.assertIn("nuevo texto", contenido)

        respaldo = os.path.join(self.temp_dir.name, "editable_bak.txt")
        self.assertTrue(os.path.exists(respaldo))

    def test_editar_nota_inexistente(self):
        exito, mensaje = self.gestor.editar("falta", "contenido")

        self.assertFalse(exito)
        self.assertIn("No se encontró la nota.", mensaje)

    def test_eliminar_nota(self):
        self.gestor.guardar(Nota("para_eliminar", "texto"))

        exito, mensaje = self.gestor.eliminar("para_eliminar")

        self.assertTrue(exito)
        self.assertIn("eliminada", mensaje)
        self.assertEqual(self.gestor.leer("para_eliminar"), "Nota no encontrada.")

    def test_eliminar_nota_inexistente(self):
        exito, mensaje = self.gestor.eliminar("sin_archivo")

        self.assertFalse(exito)
        self.assertIn("No se encontró la nota.", mensaje)

    def test_contar_excluye_respaldo(self):
        self.gestor.guardar(Nota("contable", "contenido"))
        self.gestor.editar("contable", "contenido actualizado")

        self.assertEqual(self.gestor.contar(), 1)

    def test_exportar_json_crea_archivo_con_notas(self):
        self.gestor.guardar(Nota("json", "dato"))

        exito = self.gestor.exportar_json()
        self.assertTrue(exito)

        ruta_json = os.path.join(self.temp_dir.name, "exports", "notas.json")
        self.assertTrue(os.path.exists(ruta_json))

        with open(ruta_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nombre"], "json")
        self.assertIn("contenido", data[0])

    def test_exportar_json_preserva_formato_tras_editar(self):
        self.gestor.guardar(Nota("nota", "contenido inicial"))
        self.gestor.editar("nota", "contenido editado")

        self.gestor.exportar_json()
        ruta_json = os.path.join(self.temp_dir.name, "exports", "notas.json")

        with open(ruta_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nombre"], "nota")
        self.assertEqual(data[0]["contenido"], "contenido editado")
        self.assertTrue(data[0]["fecha"])

    def test_editar_restaura_contenido_si_falla_escritura(self):
        self.gestor.guardar(Nota("fallar", "texto original"))
        ruta = os.path.join(self.temp_dir.name, "fallar.txt")
        respaldo = os.path.join(self.temp_dir.name, "fallar_bak.txt")
        real_open = open

        def fake_open(path, mode="r", *args, **kwargs):
            if path == ruta and "w" in mode:
                raise OSError("fallo simulado")
            return real_open(path, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=fake_open):
            exito, mensaje = self.gestor.editar("fallar", "contenido nuevo")

        self.assertFalse(exito)
        self.assertIn("No fue posible editar la nota", mensaje)

        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        self.assertIn("texto original", contenido)
        self.assertTrue(os.path.exists(respaldo))


if __name__ == "__main__":
    unittest.main()
