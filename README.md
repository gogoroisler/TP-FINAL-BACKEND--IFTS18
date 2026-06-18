# Sistema de Administración de Consorcios
Trabajo Práctico Final — Materia Desarrollo Backend — IFTS 18

**Autores:** Gonzalez Roisler Santiago, Navarro Fernando, Rodriguez Leandro

---

## Descripción

Sistema web desarrollado en Django para la gestión integral de consorcios. Permite administrar consorcios, departamentos, titularidades, expensas, reclamos y avisos, con roles diferenciados para administradores y consorcistas.

---

## Tecnologías utilizadas

- Python 3.14
- Django 6.0.6
- SQLite3
- HTML
- Git / GitHub

---

## Arquitectura del proyecto

El proyecto sigue los siguientes patrones de diseño:

- **CBV (Class Based Views):** todas las vistas están implementadas como clases
- **RolRequeridoMixin:** controla el acceso por rol en todas las CBV
- **selectors.py por app:** todas las consultas a la base de datos están centralizadas en archivos `selectors.py`, nunca en las vistas

### Apps

| App | Responsabilidad |
|-----|----------------|
| `core` | Home, paneles de admin y consorcista |
| `consorcios` | Consorcio, Departamento, Titularidad, SolicitudVinculacion |
| `expensas` | Proveedor, GastoConsorcio, Expensa, Pago |
| `usuarios` | Perfil, RolRequeridoMixin, registro |
| `reclamos` | Reclamo |
| `avisos` | Aviso |

---

## Modelos principales

### consorcios
- **Consorcio:** nombre, dirección, CUIT, teléfono, email
- **Departamento:** consorcio, número, piso, propietario, metros cuadrados, usuario
- **Titularidad:** departamento, usuario, fecha_desde, fecha_hasta — permite registro histórico de titulares
- **SolicitudVinculacion:** usuario, consorcio, departamento, estado (pendiente/aprobada/rechazada), nota_admin

### expensas
- **Proveedor:** nombre, CUIT, rubro
- **GastoConsorcio:** consorcio, proveedor, período, descripción, monto, tipo (ordinario/extraordinario), alcance (general/por departamento), prorrateo (proporcional/igualitario)
- **Expensa:** departamento, período, monto calculado, fecha de vencimiento, estado de pago, publicada
- **Pago:** expensa, fecha, monto, nota

### usuarios
- **Perfil:** usuario (OneToOne), rol (admin/consorcista)

### reclamos
- **Reclamo:** departamento, usuario, título, descripción, estado (pendiente/en_proceso/resuelto)

### avisos
- **Aviso:** consorcio, título, contenido, activo, fecha

---

## Lógica de negocio

### Cálculo de expensas

Las expensas se calculan automáticamente a partir de los gastos del consorcio:

| Tipo | Alcance | Prorrateo | Fórmula |
|------|---------|-----------|---------|
| Ordinario | General | Proporcional | monto × (m² depto / m² totales) |
| Extraordinario | General | Proporcional | monto × (m² depto / m² totales) |
| Extraordinario | Por departamento | Proporcional | monto × (m² depto / m² involucrados) |
| Extraordinario | Por departamento | Igualitario | monto / cantidad de deptos involucrados |

### Flujo de generación de expensas

1. Admin carga los gastos del consorcio del período via Django Admin
2. Admin ingresa a `/generar-expensas/` y selecciona consorcio y período
3. El sistema muestra una vista previa con el monto calculado por departamento
4. Al confirmar, se crean las expensas con `publicada=True`
5. El consorcista las visualiza en `/mis-expensas/`

### Flujo de vinculación

1. Consorcista se registra y accede al panel
2. Solicita vinculación a un consorcio y departamento
3. Admin aprueba → se crea una Titularidad activa
4. Admin puede retirar permisos → se cierra la Titularidad (fecha_hasta = hoy)
5. Si el departamento ya tiene un titular activo, el admin puede reemplazarlo o agregar uno adicional

### Titularidad

- El sistema mantiene un registro histórico de todos los titulares de cada departamento
- Una titularidad activa tiene `fecha_hasta = null`
- Un departamento puede tener múltiples titulares activos simultáneos

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/gogoroisler/TP-FINAL-BACKEND--IFTS18.git
cd TP-FINAL-BACKEND--IFTS18
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

---

## Acceso al sistema

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home |
| `http://127.0.0.1:8000/admin/` | Django Admin |
| `http://127.0.0.1:8000/registro/` | Registro de usuarios |
| `http://127.0.0.1:8000/panel-admin/` | Panel administrador |
| `http://127.0.0.1:8000/panel-consorcista/` | Panel consorcista |

---

## Funcionalidades por rol

### Administrador
- Gestionar consorcios, departamentos y proveedores via Django Admin
- Aprobar, rechazar y gestionar solicitudes de vinculación
- Retirar permisos a consorcistas
- Cargar gastos del consorcio por período y proveedor
- Generar expensas con vista previa y cálculo automático
- Ver y gestionar todas las expensas
- Actualizar el estado de los reclamos
- Crear y gestionar avisos por consorcio

### Consorcista
- Solicitar vinculación a un consorcio y departamento
- Ver sus expensas e informar pagos
- Crear y ver sus reclamos
- Ver los avisos activos de su consorcio

---

## Seguridad

- Login requerido en todas las rutas protegidas
- Control de acceso por rol mediante `RolRequeridoMixin`
- Protección CSRF en todos los formularios
- Logout mediante POST
- Redirección automática según rol al iniciar sesión

---

## Mejoras futuras

- Página de confirmación separada para conflictos de titularidad (UX)
- Estilos visuales con Bootstrap
- API REST con Django REST Framework

---

## Licencia

Proyecto académico desarrollado con fines educativos.
