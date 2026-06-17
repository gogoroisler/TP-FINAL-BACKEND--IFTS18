# Estado del TP Final - Gestion Consorcios

## Repo de trabajo
~/Escritorio/tpfinalborrador
Rama: borrador -> sube a TP-FINAL-BACKEND--IFTS18

## Correcciones según devoluciones del docente

| # | Corrección | Estado |
|---|------------|--------|
| 1 | Config con nombre del proyecto | RESUELTO |
| 2 | Modelos separados por app | RESUELTO |
| 3 | Queries en selectors.py | RESUELTO |
| 4 | Registro histórico de titulares | RESUELTO |
| 5 | Apertura de expensas por proveedor | RESUELTO |
| 6 | Vistas basadas en clases CBV | RESUELTO |

## Funcionalidades implementadas

| Funcionalidad | Estado |
|---------------|--------|
| Login / logout / protección de rutas | OK |
| Roles admin / consorcista | OK |
| Redirect automático según rol al loguearse | OK |
| Manejo de usuarios sin Perfil | OK |
| CRUD expensas (admin) | OK |
| Gastos por proveedor (GastoConsorcio) | OK |
| Gastos ordinarios y extraordinarios | OK |
| Prorrateo proporcional / igualitario por m2 | OK |
| Validación de formato YYYY-MM en período | OK |
| Cálculo automático de expensa por departamento | OK |
| Selector de consorcio y período para generar expensas | OK |
| Vista previa antes de enviar expensas | OK |
| Envío de expensas a consorcistas | OK |
| Mis expensas (vista consorcista) | OK |
| Informar pago | OK |
| Histórico de titularidad por departamento | OK |
| Panel admin con links a funcionalidades | OK |
| Panel consorcista con links a funcionalidades | OK |
| RolRequeridoMixin reutilizable | OK |

## Estructura de modelos
- consorcios/models.py -> Consorcio, Departamento, Titularidad
- expensas/models.py   -> Proveedor, GastoConsorcio, Expensa
- usuarios/models.py   -> Perfil (roles: admin / consorcista)
- core/models.py       -> vacio

## Estructura de selectors
- consorcios/selectors.py -> get_departamento_por_usuario, get_titularidad_activa, get_departamento_por_titularidad, get_titular_en_periodo
- expensas/selectors.py   -> get_todas_las_expensas, get_expensas_por_departamento, get_expensa_por_id, get_gastos_por_consorcio_periodo, calcular_monto_departamento, generar_preview_periodo, get_resumen_gastos_periodo
- usuarios/selectors.py   -> get_perfil_por_usuario

## Estructura de vistas (CBV)
- core/views.py       -> home, PanelAdminView, PanelConsorcistView
- consorcios/views.py -> MisExpensasView, informar_pago
- expensas/views.py   -> ListarExpensasView, DetalleExpensaView, CrearExpensaView, EditarExpensaView, EliminarExpensaView, SeleccionarPreviewView, PreviewPeriodoView, enviar_expensas
- usuarios/views.py   -> redirigir_segun_rol
- usuarios/mixins.py  -> RolRequeridoMixin

## URLs
- gestion_consorcios/urls.py -> todas las rutas apuntan a sus CBV
- LOGIN_REDIRECT_URL -> /redirigir/ (redirect automatico segun rol)

## Pendientes

### Media prioridad
- [ ] Registro de usuarios desde el frontend

### Consideraciones MVP
- [ ] Historial de pagos (fecha y monto, no solo booleano)
- [ ] Módulo de reclamos (mencionado en README)
- [ ] Avisos/novedades del admin al consorcio

### Después del CSS
- [ ] Mejorar templates con estilos
- [ ] README actualizado con nuevas funcionalidades
