# Hoja de ruta — Sistema de Gestión de Consorcios

## Etapa 1 — Completar el núcleo de negocio

**1. Expensas: estado de pago real**
El modelo actual tiene `pagada` como booleano, pero ya permite pagos parciales. El campo debería calcularse automáticamente comparando la suma de pagos contra el monto total, y mostrar el saldo pendiente en la vista del consorcista.

**2. Notificaciones por email**
Hoy no existe ningún canal de comunicación automática. Con el sistema de email de Django (sin librerías externas) se puede notificar al consorcista cuando su solicitud es aprobada/rechazada, cuando vence una expensa, o cuando cambia el estado de su reclamo.

**3. Reclamos: comentarios y categorías**
El modelo actual es muy básico. Agregarle categorías (rotura, ruido, limpieza, plagas...) y un sistema de respuestas entre admin y consorcista lo convierte en un canal de comunicación real en lugar de un simple formulario de queja.

---

## Etapa 2 — Operación y visibilidad

**4. Dashboard con métricas**
El panel admin hoy es solo links de navegación. Un dashboard real mostraría: total adeudado, expensas vencidas, reclamos sin resolver, solicitudes pendientes — todo con datos reales de la base de datos.

**5. Reportes exportables**
Listar expensas en pantalla está bien, pero el admin necesita exportar: estado de deuda por departamento, composición de gastos por período, listado de morosos. Formatos: PDF y/o Excel.

**6. Paginación y filtros en listados**
Con pocos datos no se nota, pero listar expensas o reclamos sin paginar ni filtrar no escala. Django tiene paginación nativa y es trabajo menor.

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

## Lo que está sólido y no se toca

- Arquitectura (CBV + selectors + RolRequeridoMixin) bien pensada y escalable.
- Flujo de vinculación con manejo de conflictos de titulares correctamente resuelto.
- Cálculo de expensas con los 4 casos de prorrateo (ordinario/extraordinario × proporcional/igualitario).
- Diseño con Tailwind CSS aplicado en todos los templates.
