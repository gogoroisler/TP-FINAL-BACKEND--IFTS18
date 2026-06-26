---
name: contexto-tp
description: Contexto completo del TP Final de Backend IFTS 18. Usalo al inicio de cualquier sesión de trabajo en este proyecto para no tener que re-descubrir la arquitectura, decisiones de diseño y estado actual.
---

# Contexto del TP Final — Sistema de Gestión de Consorcios

**Materia:** Desarrollo Backend — IFTS 18
**Autores:** Gonzalez Roisler Santiago, Navarro Fernando, Rodriguez Leandro
**Stack:** Python 3.14 / Django 6.0.6 / SQLite3 / Tailwind CSS via CDN
**Rama de trabajo:** `borrador`
**Remote correcto:** `tpfinal` → `https://github.com/gogoroisler/TP-FINAL-BACKEND--IFTS18.git`
(hay un segundo remote `origin` que apunta a otro repo — ignorarlo para pushes)

---

## Arquitectura

### Patrones centrales

- **CBV exclusivamente:** todas las vistas son clases (ListView, CreateView, UpdateView, DeleteView). Nunca vistas de función salvo casos puntuales ya existentes (gestionar_solicitud, informar_pago, etc.)
- **selectors.py por app:** las vistas NUNCA acceden al ORM directamente. Toda consulta a la base de datos pasa por funciones en `selectors.py` de cada app
- **RolRequeridoMixin:** todas las CBV protegidas definen `rol_requerido = 'admin'` o `'consorcista'`. El mixin vive en `usuarios/mixins.py`
- **Signals para side effects:** `post_save` y `post_delete` en `Pago` actualizan `Expensa.pagada` automáticamente. Registrado en `expensas/signals.py` y cargado en `expensas/apps.py` vía `ready()`
- **Tailwind via CDN:** `<script src="https://cdn.tailwindcss.com"></script>` en `base.html`. Sin build step, sin npm

### Apps

| App | Modelos clave |
|-----|--------------|
| `consorcios` | Consorcio, Departamento, Titularidad, SolicitudVinculacion |
| `expensas` | Proveedor, GastoConsorcio, Expensa, Pago |
| `usuarios` | Perfil (OneToOne con User, rol admin/consorcista) |
| `reclamos` | Reclamo |
| `avisos` | Aviso |
| `core` | vistas de home y paneles |

---

## Modelos — decisiones importantes

### Consorcio
- `cuit`: `unique=True`

### Departamento
- `unique_together = [['consorcio', 'numero']]` — un número de dpto es único dentro de un consorcio
- **NO tiene campo `usuario`** — fue eliminado. La vinculación usuario-depto se gestiona exclusivamente a través de `Titularidad`

### Titularidad
- `fecha_hasta = null` → titularidad activa
- `condicion` = `'dueno'` | `'inquilino'`
- Un departamento puede tener múltiples titulares activos simultáneos
- Al crear desde el panel y ya existe titular activo → se muestra `titularidades/confirmar_crear.html` antes de proceder (dos pasos: POST detecta conflicto → segundo POST con `confirmado=1` crea)

### SolicitudVinculacion
- El campo `consorcio` se deriva automáticamente de `departamento.consorcio` en `form_valid` — no va en el formulario
- `condicion` = `'dueno'` | `'inquilino'` — se copia a `Titularidad` al aprobar
- Al aprobar con titular activo: opciones `aprobar_reemplazar` (cierra la anterior) o `aprobar_agregar` (mantiene ambas)

### Expensa
- `pagada`: booleano actualizado automáticamente por signal — NO actualizarlo a mano
- `saldo_pendiente`: property calculada → `monto - sum(pagos.monto)`
- Pagos parciales permitidos; saldo negativo = crédito a favor del consorcista
- El crédito se muestra en `/mis-expensas/` descontado del saldo de expensas impagas

### Proveedor
- `cuit`: `unique=True`

---

## URLs — estructura principal

```
/consorcios/          listar_consorcios
/consorcios/nuevo/    crear_consorcio
/departamentos/       listar_departamentos
/titularidades/       listar_titularidades
/gastos/              listar_gastos
/proveedores/         listar_proveedores
/perfiles/            listar_perfiles
/usuarios/            listar_usuarios
/panel-admin/         panel_admin
/panel-consorcista/   panel_consorcista
/mis-expensas/        mis_expensas
/crear-reclamo/       crear_reclamo
/mis-reclamos/        mis_reclamos
/solicitud/           crear_solicitud
/solicitudes/         listar_solicitudes
/generar-expensas/    generar_expensas
```

Archivo de URLs: `gestion_consorcios/urls.py`

---

## Templates

- Todos extienden `base.html`
- Estructura: `templates/{app}/accion.html` (ej: `templates/consorcios/crear.html`)
- Los forms de Django necesitan este bloque CSS inline para verse con Tailwind:
  ```html
  <style>
    #content input, #content select { border:1px solid #cbd5e1; border-radius:6px; padding:8px 12px; width:100%; font-size:14px; outline:none; }
    #content input:focus, #content select:focus { border-color:#10b981; box-shadow:0 0 0 2px rgba(16,185,129,0.2); }
  </style>
  ```
- Los errores `unique_together` van en `form.non_field_errors`, no en `field.errors` — siempre renderizar ambos en formularios de creación/edición

---

## Flujos de negocio

### Vinculación consorcista
1. Consorcista crea solicitud eligiendo departamento + condición (dueño/inquilino)
2. Admin aprueba/rechaza en `/solicitudes/`
3. Al aprobar: se crea `Titularidad` con `condicion` copiado de la solicitud
4. Si hay titular activo: admin ve conflicto, elige reemplazar o agregar
5. Admin puede retirar permisos → `fecha_hasta = hoy` en la titularidad

### Generación de expensas
1. Admin carga gastos del período en `/gastos/nuevo/`
2. Admin va a `/generar-expensas/`, selecciona consorcio y período
3. Vista previa con montos por departamento
4. Al confirmar: se crean expensas con `publicada=True`
5. Consorcista ve sus expensas en `/mis-expensas/`

### Pago de expensas
- `informar_pago` (función en `consorcios/views.py`) crea un `Pago`
- El signal actualiza `expensa.pagada` automáticamente
- Pagos parciales → `saldo_pendiente > 0`, `pagada=False`
- Sobrepago → `saldo_pendiente < 0` = crédito disponible para el consorcista

---

## Selectores relevantes

```python
# consorcios/selectors.py
get_departamento_por_titularidad(usuario)   # depto activo del consorcista
get_titularidad_activa_por_departamento(departamento)
get_titularidades_activas_por_departamento(departamento)
get_titularidades_activas_por_usuario(usuario)  # todas las titularidades activas del usuario (select_related depto__consorcio)
get_todos_los_consorcios()
get_todos_los_departamentos()
get_todas_las_titularidades()
get_todas_las_solicitudes()
get_solicitud_por_usuario(usuario)

# expensas/selectors.py
get_expensas_por_departamento(departamento)
get_todas_las_expensas()                    # con select_related depto__consorcio, order_by -periodo
get_pagos_por_expensa(expensa)
get_credito_disponible(departamento)        # suma saldos negativos de expensas impagas
get_detalle_gastos_por_expensa(expensa)     # devuelve {'detalle': [...], 'total_consorcio': Decimal}
get_todos_los_proveedores()
get_todos_los_gastos()

# usuarios/selectors.py
get_perfil_por_usuario(usuario)
get_todos_los_perfiles()
get_todos_los_usuarios()
```

---

## Migraciones existentes

```
consorcios: 0001→0007
  0004: add condicion to SolicitudVinculacion
  0005: unique_together Departamento + unique Consorcio.cuit
  0006: add condicion to Titularidad
  0007: remove usuario from Departamento

expensas: 0001→0003
  0003: unique Proveedor.cuit
```

---

## Lo que ESTÁ implementado (no repetir)

- CRUD completo (sin Django Admin) para: Consorcios, Departamentos, Titularidades, Proveedores, Gastos, Perfiles, Usuarios
- Signal post_save + post_delete en Pago → actualiza Expensa.pagada
- Crédito disponible por sobrepago mostrado en mis_expensas
- Condición dueño/inquilino en SolicitudVinculacion y Titularidad
- Confirmación al crear Titularidad con conflicto (dos pasos)
- Unique constraints: Consorcio.cuit, Proveedor.cuit, Departamento(consorcio+numero)
- Error reclamo sin departamento: mensaje amigable, no 500
- Detalle de expensa para el consorcista (`/mis-expensas/<id>/`): composición de gastos del período con contribución por departamento, historial de pagos, botón imprimir/PDF (window.print + @media print)
- Filtros GET en todos los listados del admin: expensas (consorcio/período/departamento), reclamos (consorcio/estado), avisos (consorcio), gastos (consorcio/proveedor/período), departamentos (consorcio), titularidades (consorcio/departamento con dropdown cascading via onchange)
- Listado de usuarios con columna "Vinculaciones activas" (Prefetch con to_attr) y filtros por rol, consorcio y departamento
- Documentación completa: README.md, ROADMAP.md, DECISIONES.md (arquitectura, modelo, lógica, bugs, filtros, uso de IA)

## Lo que falta (ver ROADMAP.md)

- Notificaciones por email
- Reclamos con comentarios y categorías
- Dashboard con métricas reales
- Reportes exportables para el admin (PDF/Excel)
- Paginación en listados
- Registro de auditoría
- API REST
- Tests automatizados
- Sistema de crédito automático entre períodos (hoy se muestra pero no se descuenta al generar)
- Múltiples vinculaciones y desvinculación por el consorcista
