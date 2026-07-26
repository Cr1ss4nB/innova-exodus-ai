# Innova Exodus

Innova Exodus es un asistente corporativo inteligente basado en Inteligencia Artificial y Retrieval-Augmented Generation (RAG), desarrollado para responder preguntas en lenguaje natural a partir de la documentación interna de una empresa. El sistema permite gestionar documentos mediante una interfaz sencilla, procesarlos e indexarlos para ofrecer respuestas precisas basadas exclusivamente en la información disponible.

---

## Acerca del Proyecto

Este proyecto fue desarrollado como solución al Challenge Alura Agente de la formación Tech Builder del programa Oracle Next Education (ONE) G10 en colaboración con Alura Latam.

El objetivo del desafío consiste en construir un agente de inteligencia artificial capaz de responder preguntas en lenguaje natural utilizando exclusivamente la información contenida en la documentación interna de una organización, aplicando técnicas de Retrieval-Augmented Generation (RAG) y desplegando la solución en Oracle Cloud Infrastructure (OCI).

---

## Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Stack Tecnológico](#stack-tecnológico)
- [Inteligencia Artificial](#inteligencia-artificial)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Despliegue en Oracle Cloud Infrastructure (OCI)](#despliegue-en-oracle-cloud-infrastructure-oci)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Autor](#autor)
- [Licencia](#licencia)

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

```text
                    Usuario
                       │
                       ▼
        Frontend (HTML, CSS y JavaScript)
                       │
                 HTTP (API REST)
                       │
                       ▼
              Backend (FastAPI)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Gestión de      Procesamiento     Recuperación
 documentos         de PDFs        de contexto
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              Generación de embeddings
                       │
                       ▼
               Índice vectorial FAISS
                       │
                       ▼
              Google Gemini (LLM)
                       │
                       ▼
        Respuesta con referencias documentales
```

### Flujo de funcionamiento

1. El usuario carga uno o varios documentos PDF desde la interfaz.
2. El backend procesa automáticamente cada documento y extrae su contenido.
3. El contenido se divide en fragmentos y se generan embeddings para cada uno de ellos.
4. Los embeddings se almacenan en un índice vectorial FAISS para permitir búsquedas semánticas.
5. Cuando el usuario realiza una consulta, el sistema recupera los fragmentos más relevantes de la documentación.
6. Dichos fragmentos se envían como contexto al modelo Google Gemini mediante un pipeline RAG (Retrieval-Augmented Generation).
7. Finalmente, el asistente genera una respuesta basada únicamente en la información recuperada y muestra las referencias de los documentos utilizados.

[Volver a la tabla de contenidos](#tabla-de-contenidos)

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

El proyecto está organizado en módulos independientes para facilitar su mantenimiento, escalabilidad y comprensión. A continuación, se describen las carpetas principales del repositorio:

- **backend/**: contiene la API REST desarrollada con FastAPI, el procesamiento de documentos, el pipeline RAG, la indexación mediante FAISS y la integración con Google Gemini.
- **frontend/**: aplicación web desarrollada con HTML, CSS y JavaScript encargada de la interfaz de usuario, la gestión de documentos y la interacción con el asistente.
- **docs/**: documentación técnica elaborada durante el desarrollo del proyecto.
- **resources/**: documentos corporativos de ejemplo utilizados para alimentar la base de conocimiento durante las pruebas y demostraciones.
- **.github/**: configuración de GitHub Actions para la automatización del despliegue del proyecto.
- **README.md**: documentación principal del proyecto.

### Árbol del proyecto

```
innova-exodus-ai/
├── .gitignore
├── LICENSE
├── README.md
├── .github/
│   ├── workflows
│   │   ├── deploy.yml
├── backend/
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── chat.py
│   │   │       ├── documents.py
│   │   │       ├── health.py
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── error_handlers.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── document.py
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── farewell_prompt.py
│   │   │   ├── greeting_prompt.py
│   │   │   └── system_prompt.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── chain.py
│   │   │   ├── embeddings/
│   │   │   │   ├── __init__.py
│   │   │   │   └── gemini_embeddings.py
│   │   │   ├── intent.py
│   │   │   ├── loaders/
│   │   │   │   ├── __init__.py
│   │   │   │   └── pdf_loader.py
│   │   │   ├── retriever.py
│   │   │   ├── splitters/
│   │   │   │   ├── __init__.py
│   │   │   │   └── text_splitter.py
│   │   │   └── vector_store/
│   │   │       ├── __init__.py
│   │   │       └── faiss_store.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── chat_schemas.py
│   │   │   └── document_schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py
│   │   │   ├── document_processing_service.py
│   │   │   ├── document_registry_service.py
│   │   │   └── document_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_hashing.py
│   │       ├── file_storage.py
│   │       └── file_validation.py
│   ├── data/
│   │   └── vector_store/
│   │       └── .gitkeep
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── test_chain.py
│       ├── test_error_handlers.py
│       ├── test_faiss_store.py
│       ├── test_file_hashing.py
│       ├── test_intent.py
│       └── test_text_splitter.py
├── docs/
│   ├── arquitectura.md
│   ├── decisiones-tecnicas.md
│   ├── desarrollo.md
│   ├── despliegue.md
│   ├── estructura-del-proyecto.md
│   ├── proyecto.md
│   └── stack-tecnologico.md
├── frontend/
│   ├── assets/
│   │   └── logo.png
│   ├── css/
│   │   ├── base.css
│   │   ├── chat.css
│   │   ├── components.css
│   │   ├── layout.css
│   │   ├── sidebar.css
│   │   └── tokens.css
│   ├── index.html
│   └── js/
│       ├── components/
│       │   ├── chatInput.js
│       │   ├── chatWindow.js
│       │   ├── confirmDialog.js
│       │   ├── documentItem.js
│       │   ├── messageBubble.js
│       │   ├── sidebar.js
│       │   ├── toast.js
│       │   └── uploader.js
│       ├── config.js
│       ├── main.js
│       ├── services/
│       │   └── apiClient.js
│       ├── state/
│       │   ├── chatStore.js
│       │   └── documentsStore.js
│       ├── types.js
│       └── utils/
│           ├── dom.js
│           ├── errors.js
│           ├── formatters.js
│           └── markdown.js
└── resources/
    └── documents/
        ├── Arquitectura-Tecnologica-Corporativa-Innova-Exodus.pdf
        ├── Arquitectura-de-Microservicios-y-Mapa-de-Dominios.pdf
        ├── FAQ-Corporativo.pdf
        ├── Guia-Oficial-de-Ingenieria-Backend-Innova-Exodus.pdf
        ├── Guia-Oficial-de-Ingenieria-Frontend-Innova-Exodus.pdf
        ├── Manual-de-Onboarding-para-Nuevos-Colaboradores-Innova-Exodus.pdf
        └── Protocolo-de-Respuesta-a-Incidentes-y-Post-Mortems-Innova-Exodus.pdf

```

[Volver a la tabla de contenidos](#tabla-de-contenidos)

---

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de contar con los siguientes requisitos:

- **Python 3.10 o superior** (se recomienda Python 3.11).
- **Git** instalado para clonar el repositorio.
- **Una API Key de Google Gemini**, necesaria para utilizar el modelo de lenguaje.
- **Conexión a Internet**, requerida para consumir la API de Gemini.

Además, antes de iniciar la aplicación deberás crear un archivo `.env` dentro de la carpeta `backend/`, tomando como referencia el archivo `.env.example` incluido en el proyecto.

> **Importante:** Sin una API Key válida de Google Gemini el asistente no podrá generar respuestas, aunque el resto de la aplicación funcione correctamente.
---

## Instalación

Sigue los siguientes pasos para obtener una copia del proyecto en tu equipo.

### 1. Clonar el repositorio

Abre una terminal o el IDE de tu preferencia (Visual Studio Code, Cursor, PyCharm, etc.) y clona el repositorio.

```bash
git clone https://github.com/Cr1ss4nB/innova-exodus-ai.git
```

Ingresa a la carpeta del proyecto.

```bash
cd innova-exodus-ai
```

---

### 2. Abrir el proyecto

Abre la carpeta del proyecto desde tu editor de código favorito.

Por ejemplo, con Visual Studio Code:

```bash
code .
```

---

### 3. Abrir dos terminales

Durante el desarrollo se utilizan dos terminales independientes:

- **Terminal 1:** Backend (FastAPI).
- **Terminal 2:** Frontend (Servidor HTTP).

---

### 4. Preparar el entorno virtual del Backend

Desde la primera terminal ingresa a la carpeta del backend.

```bash
cd backend
```

Crea un entorno virtual.

**Windows**

```bash
python -m venv .venv
```

**Linux / macOS**

```bash
python3 -m venv .venv
```

---

### 5. Activar el entorno virtual

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Si la activación fue correcta, la terminal mostrará el prefijo:

```text
(.venv)
```

---

### 6. Actualizar pip

Con el entorno virtual activo, actualiza el administrador de paquetes.

```bash
python -m pip install --upgrade pip
```

---

### 7. Instalar las dependencias

Instala todas las librerías necesarias para ejecutar el backend.

```bash
pip install -r requirements.txt
```

Una vez finalizada la instalación, el proyecto estará listo para configurarse.

---

## Configuración

Antes de ejecutar la aplicación es necesario configurar la variable de entorno que permite acceder al modelo de Inteligencia Artificial de Google Gemini.

### 1. Crear el archivo de configuración

Dentro de la carpeta `backend` encontrarás un archivo llamado:

```text
.env.example
```

Crea una copia de este archivo y renómbrala como:

```text
.env
```

La estructura quedará así:

```text
backend/
├── .env
└── .env.example
```

---

### 2. Configurar la API Key de Google Gemini

Abre el archivo `.env` y reemplaza el valor correspondiente por tu propia API Key.

```env
GEMINI_API_KEY=TU_API_KEY
```

> Puedes obtener una API Key gratuita desde Google AI Studio.

---

### 3. Verificar la configuración

Asegúrate de que:

- El archivo `.env` se encuentre dentro de la carpeta `backend`.
- La variable `GEMINI_API_KEY` tenga un valor válido.
- El entorno virtual (`.venv`) continúe activo antes de ejecutar el backend.

Una vez realizada esta configuración, el proyecto estará listo para ejecutarse.

---

## Ejecución

Una vez completadas la instalación y configuración, ya es posible iniciar el backend y el frontend.

### 1. Iniciar el Backend

Desde la primera terminal, verifica que te encuentras dentro de la carpeta `backend` y que el entorno virtual continúa activo.

La terminal debe verse similar a:

```text
(.venv) .../backend$
```

Inicia el servidor FastAPI ejecutando:

```bash
uvicorn app.main:app --reload
```

Si todo fue correcto, el backend quedará disponible en:

```text
http://localhost:8000
```

La documentación interactiva de la API (Swagger UI) estará disponible en:

```text
http://localhost:8000/docs
```

No cierres esta terminal mientras utilices la aplicación.

---

### 2. Iniciar el Frontend

Abre la segunda terminal e ingresa a la carpeta `frontend`.

```bash
cd frontend
```

Inicia un servidor HTTP local con Python.

```bash
python -m http.server 5500
```

El frontend quedará disponible en:

```text
http://localhost:5500
```

---

### 3. Abrir la aplicación

Abre tu navegador e ingresa a:

```text
http://localhost:5500
```

Desde esta interfaz podrás:

- Cargar documentos PDF.
- Visualizar los documentos cargados.
- Eliminar documentos.
- Consultar al asistente mediante lenguaje natural.
- Visualizar las fuentes utilizadas para generar cada respuesta.

---

### 4. Primera prueba

Una vez abierta la aplicación, puedes realizar las siguientes pruebas para verificar que todo funciona correctamente.

1. Envía un saludo como **"Hola"**.
2. Carga uno o varios documentos PDF desde la barra lateral. Los documentos de la empresa ficticia Innova Exodus se encuentran en "resources/documents", aunque igualmente se pueden cargar los archivos desde la interfaz con el botón **"Cargar documentación corporativa"**.
3. Espera a que finalice el proceso de indexación.
4. Realiza una pregunta relacionada con la documentación cargada.
5. Verifica que la respuesta incluya las referencias a los documentos utilizados.
6. Prueba preguntas de seguimiento como **"¿Y qué más?"**, **"Explícalo mejor"** o **"Resúmelo"** para comprobar el funcionamiento del historial conversacional temporal.

Si todas estas acciones funcionan correctamente, la aplicación estará lista para utilizarse.

[Volver a la tabla de contenidos](#tabla-de-contenidos)

---

## Ejemplos de Uso

A continuación se presentan algunos ejemplos de interacción con el asistente corporativo **Innova Exodus AI**. Las imágenes mostradas corresponden al funcionamiento real de la aplicación.

### Ejemplo 1. Saludos predefinidos

**Mensaje**

> Hola

**Respuesta**

> ¡Hola! Soy el asistente corporativo de Innova Exodus. Puedes preguntarme sobre la documentación interna de la empresa y con gusto te ayudo.

> <img width="1917" height="935" alt="saludos" src="https://github.com/user-attachments/assets/724c94df-dc66-41f7-80b6-75ac43407582" />

Así mismo con mensajes de despedida o agradecimiento. 
Este tipo de mensajes no utilizan el modelo de lenguaje para generar estas respuestas, con el fin de evitar el consumo innecesario de tokens.

> <img width="1491" height="933" alt="ejemplos" src="https://github.com/user-attachments/assets/29cd2d45-ad17-4cb6-b509-d11e2e27f1ec" />

---

### Ejemplo 2. Consulta sin documentación cargada

**Pregunta**

> ¿Qué tecnologías utiliza el backend de la empresa?

**Respuesta**

> *No cuento con información suficiente en la documentación disponible para responder esta pregunta.*

> <img width="1917" height="933" alt="image" src="https://github.com/user-attachments/assets/70816567-879c-4a7d-b309-8ea428685632" />

---

### Ejemplo 3. Consulta con documentos cargados (RAG)

**Pregunta**

> ¿Qué tecnologías utiliza el backend de la empresa?

**Respuesta**

> <img width="1917" height="936" alt="image" src="https://github.com/user-attachments/assets/a2a72e40-8c28-4ecb-9abb-07e64e4f9706" />

---

### Ejemplo 4. Pregunta de seguimiento con contexto conversacional

**Pregunta**

> ¿Y qué más sabes sobre ese stack tecnológico?

**Respuesta**

> <img width="1917" height="937" alt="image" src="https://github.com/user-attachments/assets/47eb31aa-7cd7-4715-bbf0-1cf415dd2e0a" />

El asistente comprende que la consulta hace referencia a la respuesta anterior y amplía la información utilizando nuevamente la documentación disponible, sin necesidad de repetir la pregunta completa.

[Volver a la tabla de contenidos](#tabla-de-contenidos)

---

## Despliegue en Oracle Cloud Infrastructure (OCI)

Para la publicación de Innova Exodus AI se eligió **Oracle Cloud Infrastructure (OCI)**, aprovechando su capa gratuita para alojar la aplicación de forma pública como requería el Challenge Alura Agente.

El despliegue se realizó sobre una instancia de cómputo con Ubuntu, a la que se accedió por conexión SSH para clonar el repositorio directamente desde GitHub e instalar el entorno necesario para ejecutar el proyecto.

Sobre esa instancia:

- **Nginx** se configuró como servidor web y proxy inverso: sirve el frontend de forma directa y redirige las peticiones de la API hacia el backend, permitiendo que ambos convivan bajo el mismo dominio sin problemas de CORS.
- El **backend (FastAPI/Uvicorn)** se ejecuta como un **servicio administrado con systemd**, lo que garantiza que permanezca activo de forma permanente, se reinicie automáticamente ante cualquier fallo y arranque solo al reiniciar la instancia, sin depender de mantener una sesión abierta.
- Se configuró **HTTPS mediante Certbot (Let's Encrypt)**, integrado directamente con Nginx, obteniendo un certificado SSL válido y con renovación automática.
- Para acceder mediante un nombre amigable en lugar de la dirección IP, se utilizó **DuckDNS**, un servicio gratuito de subdominios, sobre el cual se emitió el certificado HTTPS.

Como resultado, la aplicación completa (frontend, backend, pipeline RAG y chat) queda disponible públicamente a través de un dominio propio y seguro, accesible desde cualquier navegador sin configuración adicional.

### Evidencias del despliegue

> <img width="1917" height="935" alt="image" src="https://github.com/user-attachments/assets/cb5c0158-9ba3-4ed3-9310-1bbd63d8e479" />

Instancia de cómputo `innova-exodus-vm` en estado *Running*, sobre Ubuntu 20.04 (Canonical), shape `VM.Standard.E5.Flex` con 1 OCPU y 12 GB de RAM, en la región Colombia Central (Bogotá). Se muestra la IP pública `157.137.219.21` y el usuario `ubuntu` utilizado para la conexión SSH.

> <img width="1917" height="861" alt="image" src="https://github.com/user-attachments/assets/900211c6-c211-40ff-bb76-8fbf7633e6ed" />

Red virtual en la nube (VCN) `vcn-innova-exodus` con su subred pública `subnet-innova` (bloque `10.0.0.0/24`), donde se encuentra alojada la instancia de cómputo.

> <img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/be528030-58f2-4969-942b-42328f4fce9c" />

Lista de seguridad por defecto de la VCN, mostrando las reglas de ingreso configuradas para permitir tráfico TCP en los puertos 80 (HTTP) y 443 (HTTPS), además del puerto 22 (SSH) necesario para la administración remota.

> <img width="1917" height="1032" alt="image" src="https://github.com/user-attachments/assets/c23ba843-a909-4f36-a9c2-d231a6ab0b79" />

Aplicación desplegada y funcionando en `https://exodus-ai.duckdns.org`, mostrando el chat del asistente respondiendo con base en la documentación corporativa indexada, incluyendo las referencias a los documentos y páginas fuente utilizadas.

### Acceso a la aplicación

[Exodus AI](https://exodus-ai.duckdns.org/)

> Debido a las limitaciones de la capa gratuita (Free Tier) de Oracle Cloud Infrastructure, la disponibilidad de la aplicación desplegada puede variar con el tiempo. Si el enlace anterior no se encuentra disponible, el proyecto puede ejecutarse localmente siguiendo las instrucciones de instalación descritas anteriormente en este repositorio.

[Volver a la tabla de contenidos](#tabla-de-contenidos)

---

## Limitaciones conocidas

Actualmente la aplicación utiliza una única base de conocimiento compartida para todos los usuarios.

Los documentos cargados desde la interfaz se almacenan en el servidor y pasan a formar parte de la base de conocimiento utilizada por el sistema RAG, por lo que cualquier usuario que acceda a la aplicación podrá consultarlos mientras permanezcan registrados.

Esta decisión fue adoptada para mantener una arquitectura simple, sin autenticación ni gestión de usuarios, acorde con el alcance del proyecto y del Challenge.

Para realizar demostraciones, el repositorio incluye la documentación corporativa de ejemplo en la carpeta `resources/documents`, la cual puede cargarse desde la interfaz mediante el botón **"Cargar documentación corporativa"**.

Como mejora futura, podría incorporarse autenticación de usuarios y aislamiento de documentos por usuario o espacio de trabajo, permitiendo que cada usuario mantenga una base de conocimiento independiente.

---

## Autor

Cristian Andrés Basto Largo

Ingeniero de Sistemas y Computación

Universidad Pedagógica y Tecnológica de Colombia (UPTC)

Challenge hecho en la formación Tech Builder del programa Oracle Next Education (ONE) junto con Alura Latam.

---

## Licencia

MIT License
