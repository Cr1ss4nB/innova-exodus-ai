# Decisiones Técnicas

## Arquitectura

Se utilizará una arquitectura cliente-servidor separando Backend y Frontend.

---

## Backend

Se utilizará FastAPI por su rendimiento, simplicidad y facilidad para construir APIs REST.

---

## Frontend

Se desarrollará utilizando HTML, CSS y JavaScript puro.

El objetivo es mantener el proyecto ligero y sencillo.

---

## Inteligencia Artificial

El modelo de lenguaje seleccionado será Google Gemini.

La aplicación utilizará LangChain para implementar el pipeline RAG.

La búsqueda semántica utilizará FAISS como base vectorial.

---

## Gestión Documental

Los documentos serán administrados desde la propia aplicación.

Se permitirá:

- subir documentos
- eliminar documentos

No se implementará edición de documentos.

---

## Base de conocimiento

La información utilizada por el asistente provendrá únicamente de los documentos cargados por la empresa.

No se utilizará información externa.

---

## Diseño

Se priorizará la funcionalidad sobre la complejidad visual.

La interfaz será limpia, moderna y enfocada en la experiencia del usuario.

---

## Desarrollo

El proyecto será desarrollado por fases, priorizando primero el funcionamiento completo del sistema y posteriormente las mejoras visuales.