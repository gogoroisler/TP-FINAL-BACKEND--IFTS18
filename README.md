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
- HTML + Tailwind CSS (via CDN)
- Git / GitHub

---

## Arquitectura del proyecto

El proyecto sigue los siguientes patrones de diseño:

- **CBV (Class Based Views):** todas las vistas están implementadas como clases
- **RolRequeridoMixin:** controla el acceso por rol en todas las CBV
- **selectors.py por app:** todas las consultas a la base de datos están centralizadas en archivos `selectors.py`, nunca en las vistas
- **Signals de Django:** `post_save` y `post_delete` en `Pago` actualizan automáticamente el estado de `Expensa.pagada`

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
- **Consorcio:** nombre, dirección, CUIT (único), teléfono, email
- **Departamento:** consorcio, número, piso, propietario, metros cuadrados — `unique_together` en (consorcio, número)
- **Titularidad:** departamento, usuario, condición (dueño/inquilino), fecha_desde, fecha_hasta — permite registro histórico de titulares
- **SolicitudVinculacion:** usuario, consorcio (derivado del departamento), departamento, condición (dueño/inquilino), estado (pendiente/aprobada/rechazada), nota_admin

### expensas
- **Proveedor:** nombre, CUIT (único), rubro
- **GastoConsorcio:** consorcio, proveedor, período, descripción, monto, tipo (ordinario/extraordinario), alcance (general/por departamento), prorrateo (proporcional/igualitario)
- **Expensa:** departamento, período, monto calculado, fecha de vencimiento, estado de pago (`pagada`), publicada — `pagada` se actualiza automáticamente vía signals
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

1. Admin carga los gastos del consorcio del período desde `/gastos/nuevo/`
2. Admin ingresa a `/generar-expensas/` y selecciona consorcio y período
3. El sistema muestra una vista previa con el monto calculado por departamento
4. Al confirmar, se crean las expensas con `publicada=True`
5. El consorcista las visualiza en `/mis-expensas/`

### Estado de pago y pagos parciales

- El campo `Expensa.pagada` se actualiza automáticamente mediante signals de Django (`post_save` y `post_delete` en `Pago`)
- Los pagos parciales son permitidos: un pago puede ser menor al monto total de la expensa
- Si el total pagado supera el monto (`saldo_pendiente < 0`), el excedente se muestra como crédito disponible
- El crédito se descuenta automáticamente del saldo pendiente de las expensas impagas al visualizar `/mis-expensas/`

### Flujo de vinculación

1. Consorcista se registra y accede al panel
2. Solicita vinculación eligiendo departamento y condición (dueño o inquilino)
3. Admin aprueba → se crea una Titularidad activa con la condición indicada
4. Si el departamento ya tiene un titular activo, el admin puede reemplazarlo o agregar uno adicional
5. Admin puede retirar permisos → se cierra la Titularidad (`fecha_hasta = hoy`)

### Titularidad

- El sistema mantiene un registro histórico de todos los titulares de cada departamento
- Una titularidad activa tiene `fecha_hasta = null`
- Un departamento puede tener múltiples titulares activos simultáneos
- Al crear una titularidad desde el panel, si ya existe un titular activo se muestra una pantalla de confirmación antes de proceder

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/gogoroisler/TP-FINAL-BACKEND--IFTS18.git
cd TP-FINAL-BACKEND--IFTS18
git checkout borrador
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

Las migraciones ya están incluidas en el repositorio, no hace falta correr `makemigrations`.

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Asignar perfil de administrador

Entrá al Django Admin (`http://127.0.0.1:8000/admin/`) con el superusuario creado y agregá un `Perfil` con rol `admin` para ese usuario. Esto es necesario para acceder al panel de administrador del sistema por primera vez. Una vez dentro, la gestión de usuarios y perfiles se hace desde el propio sistema en `/usuarios/` y `/perfiles/`.

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

---

## Acceso al sistema

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home |
| `http://127.0.0.1:8000/admin/` | Django Admin (solo configuración inicial) |
| `http://127.0.0.1:8000/registro/` | Registro de usuarios |
| `http://127.0.0.1:8000/panel-admin/` | Panel administrador |
| `http://127.0.0.1:8000/panel-consorcista/` | Panel consorcista |

---

## Funcionalidades por rol

### Administrador
- Gestionar consorcios, departamentos, titularidades y proveedores desde el panel
- Gestionar usuarios y perfiles desde el panel (sin Django Admin)
- Aprobar, rechazar y gestionar solicitudes de vinculación
- Al aprobar, la condición (dueño/inquilino) indicada por el consorcista se traslada automáticamente a la titularidad
- Retirar permisos a consorcistas
- Cargar y gestionar gastos del consorcio por período y proveedor
- Generar expensas con vista previa y cálculo automático
- Ver y gestionar todas las expensas
- Actualizar el estado de los reclamos
- Crear y gestionar avisos por consorcio

### Consorcista
- Solicitar vinculación a un consorcio y departamento indicando su condición (dueño o inquilino)
- Ver sus expensas, informar pagos (parciales o totales) y visualizar crédito disponible
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

Ver [ROADMAP.md](ROADMAP.md) para la hoja de ruta completa.

---

## Licencia

Proyecto académico desarrollado con fines educativos.
