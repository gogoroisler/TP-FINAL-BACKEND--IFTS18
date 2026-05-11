# Trabajo Practico Final de la materia Desarrollo Backend del IFTS 18

# Sistema de Administración de Consorcios

Proyecto desarrollado en Django para la gestión de consorcios, usuarios, departamentos y expensas.

## Descripción

Este sistema permite administrar:

- Usuarios con autenticación
- Roles y permisos
- Consorcios
- Departamentos
- Expensas
- CRUD completo de expensas
- Paneles diferenciados por tipo de usuario

El proyecto fue desarrollado como TP Final utilizando Django.

---

# Tecnologías utilizadas

- Python 3
- Django 6
- SQLite3
- HTML
- Git
- GitHub

---

# Funcionalidades implementadas

## Autenticación

- Login
- Logout
- Protección de rutas
- Manejo de sesiones

## Roles

- Administrador
- Consorcista

## Consorcios

- Alta de consorcios
- Asociación de departamentos

## Departamentos

- Asociación con consorcios
- Asociación con usuarios

## Expensas

CRUD completo:

- Crear expensas
- Listar expensas
- Editar expensas
- Eliminar expensas

## Sistema multiusuario

Cada usuario puede visualizar únicamente:

- sus expensas
- su departamento

---

# Estructura del sistema

```text
Usuario
   ↓
Perfil (rol)
   ↓
Departamento
   ↓
Expensa
-```
---

# Instalación del proyecto

## 1. Clonar repositorio

```bash
git clone https://github.com/gogoroisler/TP-FINAL-BACKEND--IFTS18.git
-```

---

## 2. Ingresar al proyecto

```bash
cd TP-FINAL-BACKEND--IFTS18
```

---

## 3. Crear entorno virtual

### Linux / Ubuntu

```bash
python3 -m venv venv
```

---

## 4. Activar entorno virtual

```bash
source venv/bin/activate
```

---

## 5. Instalar dependencias

```bash
pip install django
```

---

# Configuración de base de datos

## Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Crear superusuario

```bash
python manage.py createsuperuser
```

Completar:

* username
* email
* password

---

# Ejecutar servidor

```bash
python manage.py runserver
```

---

# Acceso al sistema

## Home

```text
http://127.0.0.1:8000/
```

## Admin Django

```text
http://127.0.0.1:8000/admin
```

---

# Usuarios y permisos

## Administrador

Puede:

* administrar expensas
* crear registros
* editar registros
* eliminar registros
* visualizar todas las expensas

## Consorcista

Puede:

* iniciar sesión
* visualizar únicamente sus expensas

---

# Templates implementados

* base.html
* home.html
* registration/login.html
* panel_admin.html
* panel_consorcista.html
* mis_expensas.html
* listar_expensas.html
* crear_expensa.html
* editar_expensa.html
* eliminar_expensa.html
* sin_permiso.html

---

# Modelos implementados

## Perfil

Relaciona usuarios con roles.

## Consorcio

Representa edificios o consorcios.

## Departamento

Relaciona:

* consorcio
* propietario
* usuario

## Expensa

Incluye:

* departamento
* período
* monto
* vencimiento
* estado de pago

---

# Seguridad implementada

* Login requerido
* Protección de rutas
* Validación de roles
* Logout mediante POST
* Protección CSRF

---

# Estado actual del proyecto

## Implementado

* Sistema de autenticación
* Roles y permisos
* CRUD de expensas
* Relación entre usuarios y departamentos
* Sistema multiusuario

## Próximas mejoras

* Sistema de reclamos
* Registro de pagos
* Dashboard administrativo
* Mejoras visuales
* API REST con Django REST Framework

---

# Autor

Proyecto desarrollado por:

* Gonzalez Roisler Santiago
* Navarro Fernando
* Rodriguez Leandro
---

# Licencia

Proyecto académico desarrollado con fines educativos.

