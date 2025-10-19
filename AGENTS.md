# AGENTS.md

## Overview
Este proyecto es un **Gestor de Notas en Python** que permite crear, leer, listar, buscar, editar, eliminar, contar y exportar notas.  
Cada nota se guarda como archivo `.txt` y se puede exportar a JSON.

## Codebase layout
- `models/nota.py` → Clase `Nota` (modelo de datos).
- `services/gestor_notas.py` → Clase `GestorNotas` (CRUD, contar, exportar).
- `main.py` → CLI con menú de usuario.
- `notas/` → Carpeta de almacenamiento de notas `.txt`.
- `notas/exports/` → Carpeta para exportaciones JSON.
- `.gitignore` → Ignora `__pycache__`, entornos virtuales, `notas/` y `exports/`.

## Core concepts
- **Nota**: entidad con `nombre`, `fecha`, `contenido`.
- **GestorNotas**: maneja persistencia en disco.
- **Menú (CLI)**: punto de entrada para el usuario.

## Capabilities
- Crear, leer, listar, buscar, editar y eliminar notas.
- Contar número total de notas válidas.
- Exportar todas las notas a JSON.

## Extension guidelines
- **Persistencia** → modificar/añadir en `GestorNotas`.
- **Nuevos comandos de usuario** → añadir en `main.py`.
- **Modelo de datos** → solo `Nota`, no incluir lógica de archivos.
- Mantener codificación **UTF-8**.
- Respetar PEP8 y docstrings.

## Commit conventions
- `feat:` → nueva funcionalidad (`feat: exportar notas a JSON`).
- `fix:` → correcciones.
- `refactor:` → mejoras internas sin añadir funciones.
- `docs:` → cambios en README/AGENTS/docstrings.
- `test:` → pruebas.

## Examples
Ejemplo de salida JSON:

```json
[
  {
    "nombre": "tarea1",
    "fecha": "2025-10-19 12:05:30",
    "contenido": "Estudiar cálculo vectorial."
  }
]
