# Gestor de Notas

Pequeña aplicación de línea de comandos pensada para razonar sobre cómo organizar
una solución en capas bien definidas: el modelo de dominio (`Nota`), la capa de
servicios encargada de la persistencia (`GestorNotas`) y la interfaz principal que
solo coordina entradas y salidas del usuario.

## Objetivo

- Practicar la asignación de responsabilidades: qué pertenece al modelo, qué al
  servicio y qué a la capa que presenta resultados.
- Documentar cada decisión relevante con docstrings, mensajes claros y pruebas
  automatizadas que respalden el comportamiento esperado.

## Requisitos

- Python 3.10+ (sin dependencias externas).

## Ejecución

```bash
python main.py
```

## Estructura

```
gestor_notas/
├── main.py              # Interfaz CLI que orquesta la interacción con el usuario.
├── models/
│   └── nota.py          # Modelo de dominio: representa los datos de cada nota.
├── services/
│   └── gestor_notas.py  # Lógica de negocio y persistencia de notas en disco.
├── tests/
│   └── test_gestor_notas.py  # Pruebas unitarias sobre la capa de servicios.
└── README.md            # Documentación del objetivo y uso del proyecto.
```

## Resumen de la Lógica

- El modelo `Nota` limpia los datos y conserva la fecha de creación al instanciarse.
- El servicio `GestorNotas` centraliza la lectura/escritura de archivos, maneja
  errores de E/S y decide cómo responder ante fallos (por ejemplo, creando
  respaldos al editar o ignorando archivos auxiliares en las búsquedas).
- La interfaz (`main.py`) solo valida entradas básicas, invoca al servicio y
  muestra los mensajes devueltos, de modo que la lógica de negocio queda aislada.
- Las pruebas unitarias comprueban cada operación del servicio en un directorio
  temporal, documentando el comportamiento esperado y ofreciendo confianza para
  futuros cambios.

## Pruebas

```bash
python -m unittest discover -s tests
```

Las pruebas construyen directorios temporales para validar las operaciones de
lectura/escritura sin afectar las notas reales.
