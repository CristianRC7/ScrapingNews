# 🤖 Generador de Blogs con IA

Sistema de generación automática de artículos profesionales mediante web scraping y Ollama (Llama 3). Busca noticias en internet, extrae contenido y genera blogs periodísticos de alta calidad.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Llama3-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
  - [1. Clonar/Descargar el Proyecto](#1-clonardescargar-el-proyecto)
  - [2. Instalar Python](#2-instalar-python)
  - [3. Instalar Dependencias](#3-instalar-dependencias)
  - [4. Instalar Docker Desktop](#4-instalar-docker-desktop)
  - [5. Instalar Ollama con Llama 3](#5-instalar-ollama-con-llama-3)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración Avanzada](#-configuración-avanzada)
- [Solución de Problemas](#-solución-de-problemas)
- [Preguntas Frecuentes](#-preguntas-frecuentes)

---

## ✨ Características

### 🔍 Búsqueda Inteligente
- **Búsqueda general** en DuckDuckGo
- **Sitios preferidos** con búsqueda directa (sin intermediarios)
- **Sistema anti-spam** que evita bloqueos
- **LocalStorage** para persistencia de preferencias

### 🎯 Priorización de Fuentes
- Agrega tus sitios de noticias favoritos
- Resultados preferidos mostrados primero (⭐)
- Búsqueda directa en sitios preferidos
- Botón de mostrar/ocultar lista de preferencias

### 🤖 Generación con IA
- Usa **Ollama** con modelo **Llama 3**
- Genera artículos profesionales y periodísticos
- Basado 100% en contenido real extraído
- Prompts personalizables en `prompts.py`

### 💾 Gestión de Contenido
- Selección múltiple de fuentes
- Descarga de blogs en formato `.txt`
- Interfaz moderna y responsive
- Sin imágenes (más rápido y sin spam)

---

## 🔧 Requisitos

### Software Necesario

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| **Python** | 3.8+ | Backend del proyecto |
| **Docker Desktop** | Última versión | Ejecutar Ollama |
| **Navegador Web** | Moderno (Chrome, Firefox, Edge) | Interfaz de usuario |

### Sistema Operativo
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

### Hardware Recomendado
- **RAM**: 8 GB mínimo (16 GB recomendado para Ollama)
- **Disco**: 10 GB libres (para Ollama + modelos)
- **CPU**: 4 núcleos (para mejor rendimiento de IA)

---

## 📥 Instalación

### 1. Clonar/Descargar el Proyecto

```bash
# Opción A: Si tienes Git
git clone [https://github.com/tu-usuario/blog-generator-ia.git](https://github.com/CristianRC7/ScrapingNews.git)
cd ScrapingNews

# Opción B: Descargar ZIP
# Descarga el proyecto, descomprime y accede a la carpeta
```

### 2. Instalar Python

#### Windows:
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Marca la opción "Add Python to PATH" durante la instalación
3. Verifica la instalación:
```bash
python --version
```

#### macOS:
```bash
# Usando Homebrew
brew install python3

# Verificar
python3 --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip

# Verificar
python3 --version
```

### 3. Instalar Dependencias de Python

Desde la carpeta del proyecto:

```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

**Librerías que se instalarán:**
- `Flask==3.0.0` - Framework web
- `requests==2.31.0` - Peticiones HTTP
- `beautifulsoup4==4.12.2` - Scraping web
- `html5lib==1.1` - Parser HTML

### 4. Instalar Docker Desktop

#### Windows:

1. **Descargar Docker Desktop**:
   - Ve a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
   - Descarga la versión para Windows

2. **Requisitos previos**:
   - Windows 10/11 de 64 bits
   - WSL 2 habilitado (Docker lo instalará automáticamente)

3. **Instalación**:
   ```
   - Ejecuta el instalador descargado
   - Sigue las instrucciones del asistente
   - Reinicia tu computadora si es necesario
   ```

4. **Verificar instalación**:
   - Abre Docker Desktop desde el menú de inicio
   - Espera a que inicie (icono de Docker en la bandeja del sistema)
   - Abre terminal y ejecuta:
   ```bash
   docker --version
   docker ps
   ```

#### macOS:

1. **Descargar Docker Desktop**:
   - [Para Mac con Intel](https://desktop.docker.com/mac/main/amd64/Docker.dmg)
   - [Para Mac con Apple Silicon (M1/M2)](https://desktop.docker.com/mac/main/arm64/Docker.dmg)

2. **Instalación**:
   ```
   - Abre el archivo .dmg descargado
   - Arrastra Docker.app a la carpeta Aplicaciones
   - Abre Docker desde Aplicaciones
   - Autoriza cuando macOS lo solicite
   ```

3. **Verificar**:
   ```bash
   docker --version
   docker ps
   ```

#### Linux (Ubuntu):

```bash
# Actualizar paquetes
sudo apt update

# Instalar dependencias
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Agregar clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio de Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Agregar usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker ${USER}

# Reiniciar sesión o ejecutar
newgrp docker

# Verificar
docker --version
docker ps
```

### 5. Instalar Ollama con Llama 3

#### Opción A: Usando Docker (Recomendado)

1. **Asegúrate de que Docker Desktop esté corriendo**

2. **Descargar y ejecutar Ollama**:

```bash
# Descargar e iniciar contenedor de Ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

3. **Descargar modelo Llama 3**:

```bash
# Ejecutar Llama 3 dentro del contenedor
docker exec -it ollama ollama run llama3
```

Espera a que descargue el modelo (puede tardar varios minutos, ~4-5 GB).

4. **Verificar que funciona**:

```bash
# Deberías ver un prompt interactivo
# Escribe algo como "Hola" y presiona Enter
# Si responde, está funcionando correctamente
# Presiona Ctrl+D para salir
```

5. **Mantener Ollama corriendo en segundo plano**:

```bash
# Detener el modo interactivo (Ctrl+D)
# El contenedor seguirá corriendo en segundo plano

# Para verificar que está corriendo:
docker ps

# Deberías ver el contenedor "ollama" en la lista
```

#### Opción B: Instalación nativa (Sin Docker)

**Windows/macOS**:
1. Descarga Ollama desde [ollama.ai](https://ollama.ai/download)
2. Instala el ejecutable
3. Abre terminal y ejecuta:
```bash
ollama run llama3
```

**Linux**:
```bash
curl https://ollama.ai/install.sh | sh
ollama run llama3
```

#### Verificar que Ollama está funcionando

```bash
# Probar el endpoint de API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Hola, ¿cómo estás?"
}'
```

Si recibes una respuesta JSON, ¡Ollama está funcionando! 🎉

---

## 🚀 Uso

### Paso 1: Iniciar Ollama (si no está corriendo)

```bash
# Si usas Docker:
docker start ollama

# Verificar que está corriendo:
curl http://localhost:11434/api/tags
```

### Paso 2: Iniciar la Aplicación

```bash
# Desde la carpeta del proyecto

# Windows
python app.py

# macOS/Linux
python3 app.py
```

Deberías ver algo como:
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### Paso 3: Abrir en el Navegador

1. Abre tu navegador
2. Ve a: [http://localhost:5000](http://localhost:5000)
3. ¡Listo! Deberías ver la interfaz del generador de blogs

### Paso 4: Usar la Aplicación

#### 📌 Agregar Sitios Preferidos (Opcional)

1. En la sección "⭐ Páginas de Preferencia"
2. Escribe:
   - **Nombre**: `Nombre personalizable para identificar la pagina`
   - **URL**: `https://www.url_del_sitio.com.bo/`
3. Click en **[+ Agregar Sitio]**
4. Repite para más sitios (recomendado: máximo 3)

#### 🔍 Buscar Noticias

1. En "🔍 Buscar Noticias"
2. Escribe tu tema: `"economía bolivia 2024"`
3. Ajusta el límite de páginas: `15`
4. Click en **[Buscar]**

**Tiempo de espera**:
- Sin sitios preferidos: ~5-10 segundos
- Con 2-3 sitios preferidos: ~15-25 segundos

#### ✅ Seleccionar Fuentes

1. Revisa los resultados:
   - **⭐ Resultados de Sitios Preferidos** (aparecen primero)
   - **🌐 Resultados Generales** (después)

2. Haz click en los checkboxes de las noticias que quieras usar

3. Verás el contador: "✅ Páginas seleccionadas: X"

**Recomendación**: Selecciona entre 3-10 páginas para mejores resultados

#### ✨ Generar Blog

1. Con al menos 1 página seleccionada
2. Click en **[✨ Generar Blog]**
3. Espera mientras:
   - Extrae el contenido de cada página
   - Envía todo a Ollama
   - Ollama genera el artículo

**Tiempo de espera**: 30 segundos - 2 minutos (depende de cuántas páginas)

#### 💾 Descargar

1. Una vez generado el blog
2. Click en **[💾 Descargar TXT]**
3. Se descargará `blog.txt` con el artículo

---

## 📁 Estructura del Proyecto

```
blog-generator-ia/
│
├── app.py                  # ⚙️ Backend Flask (servidor web)
├── scraper.py              # 🔍 Motor de búsqueda y scraping
├── prompts.py              # 💬 Plantillas de prompts para IA
├── config.py               # ⚡ Configuración (delays, límites)
├── requirements.txt        # 📦 Dependencias de Python
│
├── templates/
│   └── index.html          # 🎨 Interfaz HTML
│
├── static/
│   ├── script.js           # 💻 Lógica del frontend
│   └── style.css           # 🎨 Estilos de la interfaz
│
└── README.md               # 📖 Este archivo
```

### Descripción de Archivos Clave

#### `app.py` - Servidor Backend
- Maneja rutas HTTP (`/`, `/search`, `/generate`, `/download`)
- Conecta con Ollama para generar blogs
- Coordina scraping y generación

#### `scraper.py` - Motor de Búsqueda
- Busca **directamente** en sitios preferidos (sin DuckDuckGo)
- Búsqueda general en DuckDuckGo
- Extrae contenido de páginas web
- Sistema anti-spam integrado

#### `prompts.py` - Plantillas de IA
```python
BLOG_GENERATION_PROMPT = """Eres un periodista profesional..."""

def get_blog_prompt(topic, content):
    return BLOG_GENERATION_PROMPT.format(topic=topic, content=content)
```
**Personalízalo** para cambiar el estilo de los blogs generados.

#### `config.py` - Configuración
```python
# Delays entre búsquedas
DELAY_BETWEEN_PREFERRED_SITES = (10, 15)  # segundos
DELAY_BEFORE_GENERAL_SEARCH = (10, 15)

# Resultados por sitio
MAX_RESULTS_PER_PREFERRED_SITE = 2

# User Agents (para evitar bloqueos)
USER_AGENTS = [...]
```

---

## ⚙️ Configuración Avanzada

### Personalizar el Prompt de IA

Edita `prompts.py` para cambiar cómo escribe la IA:

```python
BLOG_GENERATION_PROMPT = """Eres un [TU ROL PERSONALIZADO].

Basándote en la siguiente información, crea un [TU TIPO DE CONTENIDO]:

INFORMACIÓN:
{content}

INSTRUCCIONES:
- [Tu instrucción 1]
- [Tu instrucción 2]
- [Tu instrucción 3]

FORMATO DESEADO:
[Describe el formato]

CONTENIDO:"""
```

**Ejemplos**:
- Cambiar a estilo informal/casual
- Generar en formato de lista
- Agregar secciones específicas
- Cambiar el tono (serio, humorístico, etc.)

### Ajustar Tiempos de Espera

En `config.py`, modifica los delays:

```python
# Para búsquedas MÁS RÁPIDAS (puede causar spam)
DELAY_BETWEEN_PREFERRED_SITES = (3, 5)
DELAY_BEFORE_GENERAL_SEARCH = (3, 5)

# Para búsquedas MÁS LENTAS (sin spam garantizado)
DELAY_BETWEEN_PREFERRED_SITES = (15, 20)
DELAY_BEFORE_GENERAL_SEARCH = (15, 20)
```

### Cambiar Límites de Resultados

```python
# Más resultados por sitio preferido
MAX_RESULTS_PER_PREFERRED_SITE = 5

# Más caracteres extraídos por página
CONTENT_CHAR_LIMIT = 1000000  # 1 millón
```

### Usar Otro Modelo de Ollama

En `app.py`, línea ~59:

```python
# Cambiar de llama3 a otro modelo
response = requests.post(
    OLLAMA_URL,
    json={
        "model": "mistral",  # o "codellama", "llama2", etc.
        "prompt": prompt,
        "stream": False
    },
    timeout=120000
)
```

**Modelos disponibles en Ollama**:
- `llama3` (recomendado)
- `mistral`
- `llama2`
- `codellama`
- Ver más en: [ollama.ai/library](https://ollama.ai/library)

---

## 🔧 Solución de Problemas

### Error: "No se pudo conectar a Ollama"

**Problema**: La aplicación no puede conectarse a Ollama en `http://localhost:11434`

**Soluciones**:

1. **Verificar que Ollama está corriendo**:
```bash
# Si usas Docker:
docker ps

# Deberías ver el contenedor "ollama" en la lista
# Si no está, iniciarlo:
docker start ollama
```

2. **Verificar el endpoint**:
```bash
curl http://localhost:11434/api/tags

# Debería devolver JSON con los modelos instalados
```

3. **Reiniciar Ollama**:
```bash
# Docker:
docker restart ollama

# Nativo:
# Cierra Ollama y vuelve a abrirlo
```

### Error 202: Spam Detectado

**Problema**: DuckDuckGo bloquea las búsquedas por "spam"

**Soluciones**:

1. **Aumentar delays en `config.py`**:
```python
DELAY_BETWEEN_PREFERRED_SITES = (15, 20)
DELAY_BEFORE_GENERAL_SEARCH = (15, 20)
DELAY_AFTER_RATE_LIMIT = 30
```

2. **Reducir sitios preferidos**:
   - Usa máximo 2-3 sitios preferidos

3. **Esperar entre búsquedas**:
   - Espera 2-3 minutos entre búsquedas diferentes

4. **Cambiar IP** (avanzado):
   - Reinicia tu router
   - Usa VPN

### No Muestra Resultados Generales

**Problema**: Solo muestra resultados de sitios preferidos

**Causas y soluciones**:

1. **Ya alcanzó el límite con preferidos**:
   - Solución: Aumenta el límite de páginas (ej: 20 en vez de 10)

2. **Error 202 en búsqueda general**:
   - Revisa la consola de Python
   - Busca: "❌ Búsqueda general bloqueada"
   - Solución: Aumenta delays (ver arriba)

### Ollama es Muy Lento

**Problema**: Generación tarda más de 5 minutos

**Soluciones**:

1. **Selecciona menos páginas**:
   - Recomendado: 3-7 páginas
   - Máximo: 15 páginas

2. **Verifica recursos del sistema**:
```bash
# Ver uso de CPU/RAM por Docker
docker stats ollama
```

3. **Asigna más RAM a Docker**:
   - Docker Desktop → Settings → Resources
   - Aumenta Memory a 8 GB o más

4. **Usa un modelo más pequeño**:
   - `llama2` es más rápido que `llama3`

### Los Sitios Preferidos No Funcionan

**Problema**: No encuentra resultados en sitios preferidos

**Explicación**: No todos los sitios tienen búsqueda pública accesible

**Soluciones**:

1. **Verifica la URL del sitio**:
   - Debe ser la URL principal: `https://ejemplo.com`
   - NO URLs de artículos específicos

2. **Prueba con sitios conocidos**:
   - WordPress, Drupal y muchos CMS funcionan bien
   - Sitios de noticias grandes suelen funcionar

3. **Usa solo búsqueda general**:
   - No agregues sitios preferidos
   - La búsqueda general siempre funciona

### Error al Instalar Dependencias

**Problema**: `pip install -r requirements.txt` falla

**Soluciones**:

1. **Actualiza pip**:
```bash
python -m pip install --upgrade pip
```

2. **Instala una por una**:
```bash
pip install Flask==3.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install html5lib==1.1
```

3. **Usa entorno virtual** (recomendado):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Luego instalar
pip install -r requirements.txt
```

---

## ❓ Preguntas Frecuentes

### ¿Necesito pagar por algo?

No. Todo es 100% gratuito:
- ✅ Python: Gratis y open source
- ✅ Docker: Versión gratuita suficiente
- ✅ Ollama: Completamente gratis
- ✅ Llama 3: Modelo open source gratuito

### ¿Cuánto espacio ocupa?

- Proyecto: ~1 MB
- Docker + Ollama: ~2 GB
- Modelo Llama 3: ~4-5 GB
- **Total**: ~7 GB aproximadamente

### ¿Necesito internet?

**Durante instalación**: Sí, para descargar todo

**Durante uso**:
- Búsqueda de noticias: Sí (scraping web)
- Generación con IA: **No** (Ollama funciona localmente)

### ¿Funciona en cualquier idioma?

**Búsqueda**: Sí, puedes buscar en cualquier idioma

**Generación**: Llama 3 funciona mejor en inglés, pero puede generar en español. Para mejores resultados en español, considera usar modelos específicos.

### ¿Puedo usar otro modelo de IA?

Sí. Modifica `app.py` (línea 59) y cambia `"model": "llama3"` por:
- `mistral` - Más rápido
- `llama2` - Más compatible
- `codellama` - Para contenido técnico
- Otros en [ollama.ai/library](https://ollama.ai/library)

### ¿Es legal hacer scraping?

El scraping para uso personal y educativo generalmente es legal. Sin embargo:
- ⚠️ Respeta los `robots.txt` de los sitios
- ⚠️ No sobrecargues servidores (usa delays)
- ⚠️ No uses contenido comercialmente sin permiso
- ⚠️ Revisa términos de servicio de cada sitio

### ¿Cómo detengo el servidor?

En la terminal donde ejecutaste `python app.py`:
- Presiona `Ctrl + C`

Para detener Ollama (Docker):
```bash
docker stop ollama
```

### ¿Dónde se guardan los datos?

- **Sitios preferidos**: LocalStorage del navegador
- **Blogs generados**: Se descargan como `.txt`, no se guardan en servidor
- **Datos temporales**: Se borran al cerrar la aplicación

---

## 📝 Licencia

Este proyecto es de código abierto. Úsalo libremente para:
- ✅ Aprendizaje personal
- ✅ Proyectos educativos
- ✅ Investigación

---

## 🤝 Contribuciones

¿Encontraste un bug? ¿Tienes una mejora?

1. Reporta issues
2. Sugiere funcionalidades
3. Envía pull requests

---

## 📧 Soporte

¿Problemas no resueltos en este README?

1. Revisa la sección [Solución de Problemas](#-solución-de-problemas)
2. Busca en los issues del repositorio
3. Crea un nuevo issue con:
   - Descripción del problema
   - Pasos para reproducirlo
   - Mensajes de error (si hay)
   - Sistema operativo

---

## 🎉 ¡Gracias por usar el Generador de Blogs con IA!

**Desarrollado con ❤️ usando**:
- Python + Flask
- Ollama + Llama 3
- BeautifulSoup
- DuckDuckGo
- JavaScript + HTML + CSS


---

<div align="center">

### ⭐ Si este proyecto te fue útil, dale una estrella ⭐

**Desarrollado con ❤️ Cristian Ramirez**

</div>