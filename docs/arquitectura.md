# Arquitectura

## Arquitectura General

Innova Exodus está dividido en dos aplicaciones independientes que se comunican mediante una API REST.

- Backend
- Frontend

El Backend será responsable del procesamiento documental, la gestión de documentos, el pipeline RAG y la comunicación con el modelo de lenguaje.

El Frontend será responsable de la interacción con el usuario mediante una interfaz web tipo chat.

---

# Backend

Responsabilidades:

- Gestión de documentos.
- Procesamiento de archivos.
- Extracción de texto.
- División en fragmentos (Chunking).
- Generación de embeddings.
- Indexación vectorial.
- Recuperación semántica.
- Comunicación con el LLM.
- Exposición de la API REST.

---

# Frontend

Responsabilidades:

- Interfaz de chat.
- Gestión de documentos.
- Visualización de respuestas.
- Visualización de fuentes utilizadas.
- Comunicación con la API REST.

---

# Flujo General

1. El usuario carga un documento.
2. El Backend procesa el documento.
3. Se generan embeddings.
4. Los embeddings se almacenan en FAISS.
5. El usuario realiza una pregunta.
6. Se recuperan los fragmentos más relevantes.
7. Gemini genera la respuesta utilizando únicamente ese contexto.
8. El Backend devuelve la respuesta al Frontend.

---

# Comunicación

Frontend

↓

HTTP

↓

FastAPI

↓

Pipeline RAG

↓

Gemini

↓

Respuesta

↓

Frontend