# Innova Exodus

Innova Exodus es un asistente corporativo inteligente basado en Inteligencia Artificial y Retrieval-Augmented Generation (RAG), desarrollado para responder preguntas en lenguaje natural a partir de la documentación interna de una empresa. El sistema permite gestionar documentos mediante una interfaz sencilla, procesarlos e indexarlos para ofrecer respuestas precisas basadas exclusivamente en la información disponible.

---

## Acerca del Proyecto

Este proyecto fue desarrollado como solución al Challenge Alura Agente de la formación Tech Builder del programa Oracle Next Education (ONE) G10 en colaboración con Alura Latam.

El objetivo del desafío consiste en construir un agente de inteligencia artificial capaz de responder preguntas en lenguaje natural utilizando exclusivamente la información contenida en la documentación interna de una organización, aplicando técnicas de Retrieval-Augmented Generation (RAG) y desplegando la solución en Oracle Cloud Infrastructure (OCI).

---

## Tabla de Contenidos

- Características
- Arquitectura
- Stack Tecnológico
- Estructura del Proyecto
- Requisitos Previos
- Instalación
- Configuración
- Ejecución
- Ejemplo de Uso
- Despliegue en OCI
- Autor
- Licencia

---

## Características

- Asistente corporativo basado en Inteligencia Artificial.
- Respuestas fundamentadas exclusivamente en la documentación de la empresa.
- Utiliza la técnica Retrieval-Augmented Generation (RAG).
- Gestión de documentos mediante carga y eliminación de archivos.
- Procesamiento e indexación automática de documentos.
- Búsqueda semántica mediante embeddings.
- Interfaz web tipo chat para consultas en lenguaje natural.
- Referencias a las fuentes utilizadas en cada respuesta.
- Despliegue en Oracle Cloud Infrastructure (OCI).

---

## Arquitectura

La solución se compone de dos aplicaciones independientes que trabajan conjuntamente:

- **Backend:** API REST desarrollada con FastAPI encargada del procesamiento documental, generación de embeddings, almacenamiento vectorial, recuperación de contexto y comunicación con el modelo de lenguaje.
- **Frontend:** aplicación web encargada de la interacción con el usuario, gestión de documentos y conversación con el asistente mediante una interfaz tipo chat.

Ambas aplicaciones se comunican mediante HTTP utilizando una API REST.

---

## Stack Tecnológico

| Capa / Componente | Tecnologías |
| :--- | :--- |
| **Backend** | FastAPI, Python |
| **Frontend** | HTML, CSS, JavaScript |
| **Inteligencia Artificial (IA)** | Google Gemini, LangChain, FAISS |
| **Procesamiento de Datos** | PyMuPDF, Pandas |
| **Despliegue** | Oracle Cloud Infrastructure (OCI) |
| **Control de Versiones** | Git, GitHub |

---

## Inteligencia Artificial

- Google Gemini como modelo de lenguaje.
- LangChain para la construcción del pipeline RAG.
- FAISS como base vectorial para búsqueda semántica.
- Embeddings para representar el contenido de los documentos.
- Recuperación contextual antes de generar cada respuesta.

---

## Estructura del Proyecto

---

## Requisitos Previos

---

## Instalación

---

## Configuración

---

## Ejecución

---

## Ejemplo de Uso

### Pregunta 1

### Respuesta 1

### Pregunta 2

### Respuesta 2

---

## Despliegue en Oracle Cloud Infrastructure (OCI)

---

## Autor

Cristian Andrés Basto Largo

Ingeniero de Sistemas y Computación

Universidad Pedagógica y Tecnológica de Colombia (UPTC)

---

## Licencia

MIT License
