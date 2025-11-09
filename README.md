# 🧭 Gestor de Tareas 🧭

Aplicación web creada en **Django 5** que permite a los usuarios registrarse, iniciar sesión y gestionar tareas personales: crear, ver, editar y eliminar.  
Las tareas se almacenan **en memoria**, diferenciadas por usuario, sin base de datos persistente.

---

## Funcionalidades Principales

| Módulo | Funcionalidad |
|---------|----------------|
| **Autenticación** | Registro, inicio de sesión y cierre de sesión con el sistema `django.contrib.auth`. |
| **Tareas** | CRUD completo: listar, ver detalle, agregar, editar y eliminar tareas. |
| **Sesión y migración** | Las tareas creadas sin cuenta se asocian automáticamente al usuario tras registrarse o iniciar sesión. |
| **Interfaz** | Plantillas HTML con **Bootstrap 5**, diseño responsivo y mensajes flash de confirmación. |
| **Protección de vistas** | Solo usuarios autenticados pueden acceder a sus tareas. Cada usuario ve solo las suyas. |

---
## Estructura del proyecto

- gestor_tareas/
  - manage.py
  - requirements.txt
  - gestor_tareas/
    - settings.py  <!-- Configuración global -->
    - urls.py      <!-- Rutas principales -->
    - asgi.py
    - wsgi.py
    - __init__.py
  - tareas/
    - views.py       <!-- CRUD + registro -->
    - forms.py
    - urls.py
    - memstore.py
    - templatetags/
      - __init__.py
      - form_extras.py
    - templates/
      - tareas/
        - lista.html
        - detalle.html
        - agregar.html
        - editar.html
        - eliminar.html
  - templates/
    - base.html
    - registration/
      - login.html


---

## ⚙️ Instalación y Configuración ⚙️

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/usuario/gestor_tareas.git
cd gestor_tareas
```

2️⃣ Crear entorno virtual e instalar dependencias

python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Aplicar migraciones iniciales

python manage.py migrate

4️⃣ Ejecutar el servidor

python manage.py runserver
Luego abre en el navegador: 👉 http://127.0.0.1:8000

🔐 Variables de entorno (para producción)
En un archivo .env o variables del sistema:

DJANGO_SECRET_KEY=clave-super-secreta
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,tu-dominio.cl
DJANGO_CSRF_TRUSTED=https://tu-dominio.cl
En desarrollo puedes dejar DEBUG=1 y no definir las demás.

Pruebas
Para ejecutar los tests incluidos:

python manage.py test
Los tests comprueban:

Redirección de vistas protegidas al login.

Registro exitoso y creación automática de sesión.

Creación, edición y eliminación de tareas.

Aislamiento de tareas entre usuarios.

| Acción       | Método HTTP  | Ruta                      | Descripción                                              |
| ------------ | ------------ | ------------------------- | -------------------------------------------------------- |
| **Listar**   | `GET`        | `/`                       | Muestra todas las tareas del usuario autenticado.        |
| **Detalle**  | `GET`        | `/tarea/<int:indice>/`    | Visualiza el detalle de una tarea específica.            |
| **Agregar**  | `GET / POST` | `/agregar/`               | Permite crear una nueva tarea.                           |
| **Editar**   | `GET / POST` | `/editar/<int:indice>/`   | Modifica el título o descripción de una tarea existente. |
| **Eliminar** | `GET / POST` | `/eliminar/<int:indice>/` | Confirma y elimina una tarea.                            |


### Tecnologías Utilizadas

Python 3.13

Django 5.2

Bootstrap 5.3

SQLite (solo para sesiones y usuarios)

unittest para pruebas

### Diseño y Decisiones Técnicas

El almacenamiento de tareas en memoria permite centrarse en la lógica de vistas y formularios sin depender de modelos.

Uso de login_required para proteger vistas.

memstore.py actúa como un “micro-backend” que asocia listas de tareas a cada usuario o sesión.

Sistema de mensajes flash (django.contrib.messages) para notificaciones.

Migración automática de tareas anónimas al autenticarse.

Configuración de settings.py preparada para modo producción (variables de entorno).

✨ Proyecto diseñado y desarrollado por Tatu Vergara
🎵 Músicx · 🧠 Desarrolladorx Fullstack
💻 Bootcamp Fullstack Python / Django — 2025
