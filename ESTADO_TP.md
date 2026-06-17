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
| 4 | Titularidad (historico titulares) | RESUELTO (modelo creado en consorcios) |
| 5 | Apertura por proveedor | PENDIENTE |
| 6 | Vistas basadas en clases (CBV) | PENDIENTE - siguiente paso |

## Estructura de modelos actual
- consorcios/models.py -> Consorcio, Departamento, Titularidad
- expensas/models.py   -> Expensa
- usuarios/models.py   -> Perfil (roles: admin / consorcista)
- core/models.py       -> vacio

## Estructura de selectors actual
- consorcios/selectors.py -> get_departamento_por_usuario, get_titularidad_activa
- expensas/selectors.py   -> get_todas_las_expensas, get_expensas_por_departamento, get_expensa_por_id
- usuarios/selectors.py   -> get_perfil_por_usuario

## Vistas actuales (FBV en core/views.py - pendiente migrar a CBV)
- home
- panel_admin
- panel_consorcista
- mis_expensas
- listar_expensas
- crear_expensa
- editar_expensa
- eliminar_expensa

## URLs (gestion_consorcios/urls.py)
Todas apuntan a core.views - hay que actualizar cuando migremos a CBV

## Proximo paso
Migrar core/views.py a CBV usando:
- TemplateView -> panel_admin, panel_consorcista
- ListView     -> listar_expensas, mis_expensas
- CreateView   -> crear_expensa
- UpdateView   -> editar_expensa
- DeleteView   -> eliminar_expensa
El control de roles va en el metodo dispatch() de cada clase.
