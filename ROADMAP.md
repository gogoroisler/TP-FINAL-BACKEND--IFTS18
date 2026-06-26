# Hoja de ruta — Sistema de Gestión de Consorcios

## Etapa 1 — Completar el núcleo de negocio

**1. ~~Expensas: estado de pago real~~ ✅ Implementado**
`Expensa.pagada` se actualiza automáticamente vía signals de Django (`post_save` y `post_delete` en `Pago`). El saldo pendiente y el crédito por sobrepago se muestran en `/mis-expensas/`.

**2. Notificaciones por email**
Hoy no existe ningún canal de comunicación automática. Con el sistema de email de Django (sin librerías externas) se puede notificar al consorcista cuando su solicitud es aprobada/rechazada, cuando vence una expensa, o cuando cambia el estado de su reclamo.

**3. Reclamos: comentarios y categorías**
El modelo actual es muy básico. Agregarle categorías (rotura, ruido, limpieza, plagas...) y un sistema de respuestas entre admin y consorcista lo convierte en un canal de comunicación real en lugar de un simple formulario de queja.

---

## Etapa 2 — Operación y visibilidad

**4. Dashboard con métricas**
El panel admin hoy es solo links de navegación. Un dashboard real mostraría: total adeudado, expensas vencidas, reclamos sin resolver, solicitudes pendientes — todo con datos reales de la base de datos.

**5. Reportes exportables para el administrador**
El consorcista ya puede imprimir o descargar en PDF el detalle de su propia expensa. Lo que falta es del lado del admin: exportar el estado de deuda por departamento, la composición de gastos por período y el listado de morosos. Formatos: PDF y/o Excel.

**6. ~~Filtros en listados~~ ✅ Implementado / Paginación pendiente**
Filtros implementados en: expensas (consorcio, período, departamento), reclamos (consorcio, estado), avisos (consorcio), gastos (consorcio, proveedor, período), departamentos (consorcio), titularidades (consorcio, departamento). La paginación nativa de Django queda pendiente para cuando los volúmenes de datos lo requieran.

**7. Registro de auditoría**
Quién aprobó qué solicitud, quién cambió el estado de un reclamo, qué admin generó las expensas del período. Hoy no queda rastro de ninguna acción. Una app `auditoria` con signals de Django resuelve esto.

---

## Etapa 3 — Arquitectura y escalabilidad

**8. API REST con Django REST Framework**
Abre la puerta a una app mobile o integraciones con sistemas de pago. Ya figura en el README como mejora futura pendiente.

**9. Tests automatizados**
La lógica de cálculo de expensas (4 combinaciones de tipo/alcance/prorrateo) es exactamente el tipo de cosa que se rompe silenciosamente con cambios futuros. Un conjunto de tests unitarios protege esa lógica central.

**10. Docker + CI/CD**
Para que el proyecto pueda desplegarse en cualquier servidor sin depender del ambiente local. GitHub Actions para correr los tests automáticamente en cada push.

---

**11. Múltiples vinculaciones y desvinculación por el consorcista**
Hoy un consorcista solo puede tener una vinculación activa a la vez. La mejora implicaría permitir que un consorcista solicite vinculación a más de un departamento simultáneamente (por ejemplo, si administra dos unidades), y que pueda solicitar su propia desvinculación sin necesidad de que el admin retire los permisos manualmente. Requiere refactorizar `MisExpensasView` para agrupar expensas por departamento y actualizar la lógica de solicitudes.

**12. Sistema de crédito automático entre períodos**
Hoy el crédito por sobrepago se muestra en la vista del consorcista pero no se aplica automáticamente al generar la expensa del próximo período. La mejora implicaría un campo `credito` en `Perfil` o un modelo `CreditoConsorcista` que acumule saldos a favor y los descuente al crear nuevas expensas, sin intervención del admin.

---

## Lo que está sólido y no se toca

- Arquitectura (CBV + selectors + RolRequeridoMixin) bien pensada y escalable.
- Flujo de vinculación con manejo de conflictos de titulares correctamente resuelto.
- Cálculo de expensas con los 4 casos de prorrateo (ordinario/extraordinario × proporcional/igualitario).
- Diseño con Tailwind CSS aplicado en todos los templates.
- CRUD completo sin Django Admin: consorcios, departamentos, titularidades, proveedores, gastos, usuarios y perfiles tienen vistas propias con Tailwind.
- Detalle de expensa por consorcista: composición de gastos del período con contribución por departamento y descarga en PDF.
- Filtros en todos los listados del administrador (expensas, reclamos, avisos, gastos, departamentos, titularidades).
