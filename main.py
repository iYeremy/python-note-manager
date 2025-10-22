from models.nota import Nota
from services.gestor_notas import GestorNotas

gestor = GestorNotas()

def mostrar_menu():
    """Muestra las opciones disponibles de la aplicación en consola."""
    print("\n--- Gestor de Notas ---")
    print("1. Crear nota")
    print("2. Leer nota")
    print("3. Listar notas")
    print("4. Buscar palabra")
    print("5. Editar nota")
    print("6. Eliminar nota")
    print("7. Contar notas")
    print("8. Exportar notas a JSON")
    print("9. Exportar notas a Pickle")
    print("10. Restaurar notas desde Pickle")
    print("11. Salir")

def restaurar_desde_pickle():
    """Restaura las notas que existan en el archivo pickle al almacenamiento en disco."""
    datos = gestor.cargar_desde_pickle()
    if not datos:
        print("No se encontraron datos en notas.pkl.")
        return

    restauradas = 0
    for nombre, campos in datos.items():
        contenido = campos.get("contenido", "")
        fecha = campos.get("fecha")
        nota = Nota(nombre, contenido)
        if fecha:
            nota.fecha = fecha
        exito, _ = gestor.guardar(nota)
        if exito:
            restauradas += 1

    print(f"Se restauraron {restauradas} notas desde notas.pkl.")

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre de la nota: ").strip()
        contenido = input("Contenido: ").strip()
        if len(nombre) > 0 and len(contenido) > 5:
            nota = Nota(nombre, contenido)
            exito, mensaje = gestor.guardar(nota)
            print(mensaje)
        else:
            print("El nombre o el contenido no son válidos.")

    elif opcion == "2":
        nombre = input("Nombre de la nota: ").strip()
        print(gestor.leer(nombre))

    elif opcion == "3":
        exito, resultado = gestor.listar()
        if exito:
            print("Notas disponibles:", resultado if resultado else "No hay notas guardadas.")
        else:
            print(resultado)

    elif opcion == "4":
        palabra = input("Palabra a buscar: ").strip()
        resultados = gestor.buscar(palabra)
        if resultados:
            print("Coincidencias encontradas:", resultados)
        else:
            print("No se encontraron coincidencias.")

    elif opcion == "5":
        nombre = input("Nombre de la nota a editar: ").strip()
        nuevo = input("Nuevo contenido: ").strip()
        exito, mensaje = gestor.editar(nombre, nuevo)
        # Las operaciones del servicio definen el mensaje para centralizar el tratamiento de errores de E/S.
        print(mensaje)

    elif opcion == "6":
        nombre = input("Nombre de la nota a eliminar: ").strip()
        exito, mensaje = gestor.eliminar(nombre)
        print(mensaje)

    elif opcion == "7":
        total = gestor.contar()
        print(f"Número total de notas: {total}")

    elif opcion == "8":
        gestor.exportar_json()
        print("Notas exportadas a notas.json correctamente.")

    elif opcion == "9":
        exito = gestor.exportar_pickle()
        if exito:
            print("Notas exportadas a notas.pkl correctamente.")
        else:
            print("No fue posible exportar las notas a pickle.")

    elif opcion == "10":
        restaurar_desde_pickle()

    elif opcion == "11":
        print("Programa finalizado.")
        break

    else:
        print("Opción no válida.")
