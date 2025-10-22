# Gestor de Notas en Python

Aplicación de línea de comandos que permite crear, consultar, buscar, editar, eliminar, contar y exportar notas de texto almacenadas en disco. Cada nota se guarda como archivo `.txt` con la fecha de creación y puede exportarse a un archivo JSON o a un binario `pickle` para respaldos completos.

## Características clave
- Interfaz CLI sencilla con flujo guiado por menú interactivo.
- Persistencia en disco usando archivos de texto por nota.
- Búsqueda de palabras clave sobre todas las notas existentes.
- Edición con respaldo automático para evitar pérdida de información.
- Conteo de notas válidas y exportación a `JSON` para su posterior procesamiento.
- Exportación/recuperación en formato binario (`pickle`) mediante un repositorio dedicado (`PickleRepository`).

## Requisitos
- Python 3.10 o superior.
- No se utilizan dependencias externas; `requirements.txt` se mantiene vacío para compatibilidad con herramientas estándar.

## Instalación rápida
1. Clona este repositorio y entra en él.
2. (Opcional) Crea y activa un entorno virtual.
3. Ejecuta el programa:
   ```bash
   python main.py
   ```

## Uso del menú
Dentro de la aplicación encontrarás las siguientes opciones numeradas:
- `Crear nota`: solicita nombre y contenido; guarda la nota con la fecha actual.
- `Leer nota`: muestra en pantalla el archivo correspondiente.
- `Listar notas`: enumera los nombres disponibles (sin extensiones).
- `Buscar palabra`: devuelve los nombres de notas que contienen la cadena indicada.
- `Editar nota`: actualiza el contenido y crea un respaldo `_bak`.
- `Eliminar nota`: borra definitivamente el archivo `.txt`.
- `Contar notas`: informa cuántas notas válidas existen.
- `Exportar a JSON`: genera `notas/exports/notas.json` con todas las notas.
- `Exportar a Pickle`: crea/actualiza `notas/exports/notas.pkl` con un diccionario serializado.
- `Restaurar desde Pickle`: rehidrata las notas del archivo `notas.pkl` al almacenamiento en texto (preserva la fecha original si está disponible).
- `Salir`: cierra el programa.

## Estructura del proyecto
```text
gestor_notas/
├── AGENTS.md                 Documentación interna y pautas para colaborar.
├── main.py                   CLI que orquesta la interacción con el usuario final.
├── models/
│   └── nota.py               Modelo `Nota`: limpia entradas y fija la fecha de creación.
├── notas/                    Carpeta de trabajo donde se guardan las notas `.txt`.
│   └── exports/              Subcarpeta generada para almacenar exportaciones JSON.
├── requirements.txt          Archivo reservado para dependencias (vacío actualmente).
├── services/
│   ├── gestor_notas.py       Servicio de persistencia y reglas de negocio (CRUD, búsqueda, exportaciones).
│   └── pickle_repository.py  Repositorio especializado para leer/escribir el archivo binario `notas.pkl`.
├── tests/
│   └── test_gestor_notas.py  Pruebas unitarias que validan el comportamiento del servicio.
└── README.md                 Este documento.
```

### Cómo se relacionan los componentes
- `models/nota.py`: define la estructura y representación de cada nota que será persistida.
- `services/gestor_notas.py`: expone métodos de alto nivel (`guardar`, `leer`, `listar`, `buscar`, `editar`, `eliminar`, `contar`, `exportar_json`) que encapsulan la interacción con el sistema de archivos y los mensajes de error.
- `main.py`: actúa como capa de interfaz; recibe entradas del usuario, invoca al servicio y muestra los resultados.
- `notas/`: almacén físico del contenido generado por los usuarios. Puede versionarse o ignorarse según convenga (aparece en `.gitignore`).
- `tests/test_gestor_notas.py`: utiliza directorios temporales para asegurar que las operaciones sobre archivos son robustas y no afectan datos reales.

## Exportación de notas
Los comandos de exportación crean (si no existe) la carpeta `notas/exports/`:
- `notas.json`: arreglo de notas con `nombre`, `fecha` y `contenido`, legible por humanos y otras aplicaciones.
- `notas.pkl`: diccionario serializado usando `pickle` con todas las notas. Ventajas: snapshot completo con estructuras nativas de Python y escritura/lectura rápida; limitaciones: formato no legible, depende de la versión de Python y solo debe cargarse desde fuentes confiables.

## Pruebas automatizadas
Ejecuta la batería incluida con:
```bash
python -m unittest tests.test_gestor_notas
```

Las pruebas cubren flujos de éxito y escenarios de error (por ejemplo, fallos de escritura en disco) para garantizar la integridad de los datos.
