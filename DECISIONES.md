# Decisiones de diseño y proceso de desarrollo

Sistema de Gestión de Consorcios — TP Final Backend IFTS 18
Autores: Gonzalez Roisler Santiago, Navarro Fernando, Rodriguez Leandro

---

## 1. Arquitectura general

### Por qué CBV (Class Based Views)

Django ofrece tanto vistas de función (FBV) como vistas de clase (CBV). Elegimos CBV porque:

- Las operaciones CRUD (listar, crear, editar, eliminar) tienen una estructura muy repetitiva. Con CBV como `ListView`, `CreateView` y `DeleteView`, Django provee ese comportamiento por defecto y solo hay que configurar qué modelo y qué template usar.
- El control de acceso por rol se puede centralizar en un solo mixin (`RolRequeridoMixin`) que se hereda en cada vista, en lugar de repetir la misma verificación en cada función.
- El resultado es código más corto y consistente: una vista de listado con filtros ocupa ~30 líneas en lugar de ~60 con FBV equivalentes.

### Por qué selectors.py

Todas las consultas a la base de datos están en archivos `selectors.py` dentro de cada app, y las vistas nunca llaman al ORM directamente. La razón es separar responsabilidades:

- Las vistas deciden qué mostrar y cómo responder al usuario.
- Los selectores deciden cómo obtener los datos.

Esto tiene una ventaja práctica concreta: si en el futuro cambia la forma en que se obtiene un dato (por ejemplo, agregar un caché o cambiar un filtro), el cambio se hace en un solo lugar y todas las vistas que usan ese selector se actualizan automáticamente.

### Por qué RolRequeridoMixin

Django tiene su propio sistema de permisos, pero está pensado para permisos granulares por objeto o acción. En este proyecto el control de acceso es más simple: hay dos roles (`admin` y `consorcista`) y cada vista pertenece a uno de los dos. Crear un mixin propio fue más directo que configurar el sistema de permisos nativo de Django para este caso de uso.

---

## 2. Decisiones de modelo

### Titularidad como tabla separada (registro histórico)

La primera aproximación hubiera sido un simple FK `Departamento.usuario`. Lo descartamos porque no permite saber quién vivía en un departamento en el pasado, solo quién vive ahora. Con `Titularidad` como tabla separada con `fecha_desde` y `fecha_hasta`, el sistema mantiene un historial completo: si un departamento cambió de inquilino tres veces, los tres registros están disponibles.

Una titularidad activa tiene `fecha_hasta = null`. Al retirar permisos o reemplazar un titular, se pone `fecha_hasta = hoy` en lugar de eliminar el registro.

### Por qué se eliminó Departamento.usuario

El modelo `Departamento` tenía un campo `usuario` (FK) que originalmente se usaba como atajo para saber quién habitaba el departamento. El problema es que ese campo nunca se actualizaba cuando se creaba o cerraba una `Titularidad`, creando una doble fuente de verdad: el sistema tenía dos respuestas posibles a la pregunta "¿quién vive en este departamento?" y podían no coincidir.

La solución fue eliminar `Departamento.usuario` completamente. La única fuente de verdad para la vinculación usuario-departamento es `Titularidad`. El selector `get_departamento_por_titularidad(usuario)` centraliza esa consulta.

### Condición dueño/inquilino

El consorcista declara si es dueño o inquilino al solicitar la vinculación. Esta información viaja en `SolicitudVinculacion.condicion` y se copia a `Titularidad.condicion` cuando el admin aprueba la solicitud. La decisión de copiarla (en lugar de derivarla de la solicitud) permite que la titularidad sea un registro independiente y completo, incluso si la solicitud original fuera eliminada.

### Por qué consorcio no va en el formulario de solicitud

La primera versión del formulario de `SolicitudVinculacion` tenía dos campos: `departamento` y `consorcio`. Esto generaba un problema de validación: el usuario podía seleccionar un consorcio que no correspondiera al departamento elegido. La solución fue eliminar `consorcio` del formulario y derivarlo automáticamente en `form_valid` a partir de `departamento.consorcio`. Un departamento siempre pertenece a un solo consorcio, así que la derivación es inequívoca.

### Unique constraints

Durante el desarrollo identificamos tres casos donde el modelo no impedía datos inconsistentes:

- **Consorcio.cuit**: dos consorcios podían tener el mismo CUIT. Se agregó `unique=True`.
- **Proveedor.cuit**: ídem para proveedores. Se agregó `unique=True`.
- **Departamento (consorcio + número)**: dentro de un mismo consorcio, dos departamentos no pueden tener el mismo número. Se agregó `unique_together = [['consorcio', 'numero']]`.

Sin estas restricciones, el sistema aceptaba datos incorrectos y los errores aparecerían mucho más tarde y de forma más difícil de diagnosticar.

---

## 3. Decisiones de lógica de negocio

### Expensa.pagada: signal en lugar de property

Para saber si una expensa está pagada hay que comparar la suma de todos los pagos contra el monto total. Esto se puede implementar de tres formas:

1. **Property**: se calcula al momento de acceder al atributo. No se puede filtrar con el ORM (`Expensa.objects.filter(pagada=True)` no funciona con una property).
2. **Signal**: se calcula y se persiste en el campo `pagada` cada vez que se crea, modifica o elimina un `Pago`. Soporta filtrado con el ORM.
3. **Actualización manual en la vista**: se actualiza `pagada` cuando el usuario informa un pago. Difícil de mantener si se agregan más puntos de entrada.

Elegimos la opción de signal (`post_save` y `post_delete` en `Pago`) porque permite filtrar expensas por estado con el ORM, lo que es necesario para el administrador. La función `_recalcular_pagada` está centralizada y es usada por ambos receptores para evitar duplicación.

### Pagos parciales y crédito disponible

Decidimos no poner un tope máximo al monto de un pago: si el consorcista paga de más, el excedente queda como crédito a su favor (`saldo_pendiente < 0`). Ese crédito se muestra descontado automáticamente en la vista `/mis-expensas/`, reduciendo el saldo a pagar de las expensas impagas siguientes.

La aplicación automática del crédito al generar nuevas expensas (descuento en origen) fue descartada por ahora y quedó registrada en el ROADMAP como mejora futura, porque implicaría cambios más profundos en el flujo de generación.

### Conflicto de titulares: confirmación en dos pasos

Cuando el admin intenta crear una titularidad para un departamento que ya tiene un titular activo, el sistema no bloquea la operación automáticamente. En cambio, muestra una pantalla de confirmación con la información del titular vigente y dos opciones: reemplazarlo (cierra la titularidad anterior) o agregarlo (mantiene ambos activos, útil cuando hay dueño e inquilino simultáneamente).

La misma lógica aplica cuando el admin aprueba una solicitud de vinculación desde el listado.

---

## 4. Problemas encontrados durante el desarrollo

### NOT NULL en reclamos

Al crear un reclamo, la vista asignaba el departamento del usuario mediante un selector. Cuando ese selector no encontraba ninguna titularidad activa, devolvía `None` y Django intentaba guardar el reclamo con `departamento_id = NULL`, lo que resultaba en un error 500 (violación de la restricción NOT NULL de la base de datos).

**Solución:** agregar una validación explícita en `form_valid`: si el selector devuelve `None`, se llama a `form.add_error(None, mensaje)` y se retorna `form_invalid`. El error se muestra al usuario en lugar de explotar silenciosamente.

### Signal que no se disparaba al eliminar pagos

El signal `post_save` en `Pago` actualizaba `Expensa.pagada` correctamente al crear o modificar un pago. Pero al eliminar un pago con `Pago.objects.filter(...).delete()`, `pagada` se quedaba en `True` aunque ya no hubiera pagos suficientes.

**Causa:** `post_save` solo se dispara ante creaciones y actualizaciones, no ante eliminaciones. Esto se descubrió durante pruebas en el shell de Django.

**Solución:** agregar un receptor `post_delete` que llama a la misma función `_recalcular_pagada`. La lógica de recálculo se extrajo a una función auxiliar para no duplicar código.

### Doble campo cuit en Consorcio

Al intentar agregar `unique=True` al campo `cuit` de `Consorcio`, se añadió accidentalmente un segundo campo `cuit` en lugar de modificar el existente. La migración fallaba porque el modelo tenía dos definiciones del mismo campo.

**Solución:** editar directamente el campo original en el modelo en lugar de agregar uno nuevo, y descartar la migración incorrecta.

### non_field_errors no renderizados

Los errores de `unique_together` en Django van a `form.non_field_errors`, no a los errores de campo individuales. Los templates de departamentos solo renderizaban `field.errors`, por lo que el error "ya existe un departamento con ese número en este consorcio" no aparecía en pantalla aunque la validación funcionara correctamente.

**Solución:** agregar el bloque `{% for error in form.non_field_errors %}` en los templates de crear y editar departamento.

---

## 5. Estructura de filtros en listados

Todos los listados del administrador tienen filtros implementados mediante parámetros GET. La decisión de usar GET en lugar de POST fue para que los filtros sean bookmarkeables y se puedan compartir como URL. El patrón es consistente en todos los listados:

- La vista lee los parámetros en `get_queryset()` y aplica los filtros sobre el queryset base.
- La vista pasa las opciones disponibles al contexto en `get_context_data()`.
- El template muestra el panel de filtros como un formulario GET.
- El botón "Limpiar" solo aparece cuando hay algún filtro activo.

En los casos donde un filtro depende de otro (por ejemplo, el dropdown de departamentos depende del consorcio seleccionado), se usa `onchange="this.form.submit()"` para recargar la página con el consorcio seleccionado antes de aplicar el segundo filtro.

| Listado | Filtros disponibles |
|---------|-------------------|
| Expensas | Consorcio, Período, Departamento |
| Reclamos | Consorcio, Estado |
| Avisos | Consorcio |
| Gastos | Consorcio, Proveedor, Período |
| Departamentos | Consorcio |
| Titularidades | Consorcio, Departamento |
