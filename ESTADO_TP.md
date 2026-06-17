# Estado del TP Final - Gestion Consorcios

## Repo de trabajo
~/Escritorio/tpfinalborrador
Rama: borrador -> sube a TP-FINAL-BACKEND--IFTS18

## Puntos del docente

| # | Punto | Estado |
|---|-------|--------|
| 1 | Config con nombre del proyecto | RESUELTO |
| 2 | Modelos separados por app | RESUELTO |
| 3 | Queries en selectors.py | RESUELTO |
| 4 | Titularidad (historico titulares) | RESUELTO |
| 5 | Apertura por proveedor | RESUELTO |
| 6 | Vistas basadas en clases (CBV) | RESUELTO |

## Estructura de modelos
- consorcios/models.py -> Consorcio, Departamento, Titularidad
- expensas/models.py   -> Proveedor, Expensa, ItemExpensa
- usuarios/models.py   -> Perfil (roles: admin / consorcista)
- core/models.py       -> vacio

## Estructura de selectors
- consorcios/selectors.py -> get_departamento_por_usuario, get_titularidad_activa
- expensas/selectors.py   -> get_todas_las_expensas, get_expensas_por_departamento, get_expensa_por_id, get_items_por_expensa
- usuarios/selectors.py   -> get_perfil_por_usuario

## Estructura de vistas (CBV)
- core/views.py       -> home (FBV), PanelAdminView, PanelConsorcistView
- consorcios/views.py -> MisExpensasView
- expensas/views.py   -> ListarExpensasView, CrearExpensaView, EditarExpensaView, EliminarExpensaView

## URLs
- gestion_consorcios/urls.py -> todas las rutas apuntan a sus CBV

## Pendientes opcionales
- Integrar ItemExpensa en templates (mostrar desglose por proveedor)
- Integrar Titularidad en logica de vistas
- Mejorar templates con CSS
