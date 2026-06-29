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
- Claude Code (Anthropic) — asistencia de IA durante el desarrollo (ver [DECISIONES.md](DECISIONES.md#6-uso-de-inteligencia-artificial-en-el-desarrollo))

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

### Detalle de expensa

El consorcista puede ingresar al detalle de cada expensa en `/mis-expensas/<id>/` y ver:
- Los gastos del consorcio en ese período (proveedor, descripción, tipo, monto total)
- La contribución que le corresponde a su departamento por cada gasto, según el criterio de prorrateo aplicado
- El historial de pagos realizados y el saldo pendiente
- Un botón para imprimir o descargar el detalle como PDF directamente desde el navegador (sin dependencias externas)

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

## Referencia de URLs

### Acceso general
| URL | Descripción |
|-----|-------------|
| `/` | Home |
| `/registro/` | Registro de usuarios |
| `/panel-admin/` | Panel administrador |
| `/panel-consorcista/` | Panel consorcista |
| `/admin/` | Django Admin (solo configuración inicial de perfil) |

### Consorcista
| URL | Descripción |
|-----|-------------|
| `/solicitud/` | Solicitar vinculación a un departamento |
| `/mis-expensas/` | Ver expensas propias |
| `/mis-expensas/<id>/` | Detalle de expensa con composición de gastos |
| `/informar-pago/<id>/` | Informar pago de una expensa |
| `/crear-reclamo/` | Crear reclamo |
| `/mis-reclamos/` | Ver reclamos propios |
| `/mis-avisos/` | Ver avisos activos del consorcio |

### Administrador — Gestión
| URL | Descripción |
|-----|-------------|
| `/solicitudes/` | Listar y gestionar solicitudes de vinculación |
| `/solicitudes/<id>/` | Aprobar o rechazar una solicitud |
| `/solicitudes/retirar/<id>/` | Retirar permisos a un consorcista |
| `/consorcios/` | Listar consorcios |
| `/consorcios/nuevo/` | Crear consorcio |
| `/consorcios/editar/<id>/` | Editar consorcio |
| `/consorcios/eliminar/<id>/` | Eliminar consorcio |
| `/departamentos/` | Listar departamentos (filtro por consorcio) |
| `/departamentos/nuevo/` | Crear departamento |
| `/departamentos/editar/<id>/` | Editar departamento |
| `/departamentos/eliminar/<id>/` | Eliminar departamento |
| `/titularidades/` | Listar titularidades (filtros por consorcio y departamento) |
| `/titularidades/nuevo/` | Crear titularidad |
| `/titularidades/editar/<id>/` | Editar titularidad |
| `/titularidades/eliminar/<id>/` | Eliminar titularidad |
| `/usuarios/` | Listar usuarios |
| `/usuarios/nuevo/` | Crear usuario |
| `/usuarios/editar/<id>/` | Editar usuario |
| `/usuarios/eliminar/<id>/` | Eliminar usuario |
| `/perfiles/` | Listar perfiles |
| `/perfiles/nuevo/` | Crear perfil |
| `/perfiles/editar/<id>/` | Editar perfil |
| `/perfiles/eliminar/<id>/` | Eliminar perfil |

### Administrador — Expensas y gastos
| URL | Descripción |
|-----|-------------|
| `/gastos/` | Listar gastos (filtros por consorcio, proveedor, período) |
| `/gastos/nuevo/` | Crear gasto |
| `/gastos/editar/<id>/` | Editar gasto |
| `/gastos/eliminar/<id>/` | Eliminar gasto |
| `/proveedores/` | Listar proveedores |
| `/proveedores/nuevo/` | Crear proveedor |
| `/proveedores/editar/<id>/` | Editar proveedor |
| `/proveedores/eliminar/<id>/` | Eliminar proveedor |
| `/generar-expensas/` | Seleccionar consorcio y período para generar expensas |
| `/preview/<consorcio_id>/<periodo>/` | Vista previa del cálculo por departamento |
| `/enviar-expensas/<consorcio_id>/<periodo>/` | Confirmar y generar expensas |
| `/listar-expensas/` | Listar expensas (filtros por consorcio, período, departamento) |
| `/expensa/<id>/` | Detalle de expensa (vista admin) |

### Administrador — Reclamos y avisos
| URL | Descripción |
|-----|-------------|
| `/reclamos/` | Listar reclamos (filtros por consorcio y estado) |
| `/reclamos/actualizar/<id>/` | Actualizar estado de un reclamo |
| `/avisos/` | Listar avisos (filtro por consorcio) |
| `/avisos/nuevo/` | Crear aviso |
| `/avisos/editar/<id>/` | Editar aviso |

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
- Ver y gestionar todas las expensas con filtros por consorcio, período y departamento
- Ver reclamos con filtros por consorcio y estado; actualizar estado y agregar nota de respuesta a cada reclamo
- Ver avisos con filtro por consorcio; crear y editar avisos por consorcio
- Ver gastos con filtros por consorcio, proveedor y período
- Ver departamentos con filtro por consorcio
- Ver titularidades con filtros por consorcio y departamento
- Desactivar usuarios en lugar de eliminarlos (borrado lógico, datos conservados y recuperables)

### Consorcista
- Solicitar vinculación a un consorcio y departamento indicando su condición (dueño o inquilino)
- Ver sus expensas ordenadas por período, informar pagos (parciales o totales) y visualizar crédito disponible
- Ver el detalle de cada expensa: composición de gastos agrupada por tipo (ordinarios / extraordinarios) con subtotales y monto a pagar por departamento
- Descargar o imprimir el detalle de una expensa en PDF desde el navegador
- Crear y ver sus reclamos; ver la nota de respuesta del administrador en cada reclamo
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
