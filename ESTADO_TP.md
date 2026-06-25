# Estado del TP Final - Gestion Consorcios

## Repo de trabajo
~/Escritorio/tpfinalborrador
Rama: borrador -> sube a TP-FINAL-BACKEND--IFTS18

## Comandos útiles
cd ~/Escritorio/tpfinalborrador
source venv/bin/activate
python manage.py runserver
git add . && git commit -m "mensaje" && git push tpfinal borrador

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
| Registro de usuarios desde el frontend | OK |
| Roles admin / consorcista con RolRequeridoMixin | OK |
| Redirect automático según rol al loguearse | OK |
| Manejo de usuarios sin Perfil | OK |
| Solicitud de vinculación consorcista → admin | OK |
| Aprobación / rechazo de solicitudes | OK |
| Reenvío de solicitud tras rechazo | OK |
| Retirar permisos (cierra Titularidad activa) | OK |
| Retirar permisos con selector cuando hay múltiples titulares | OK |
| Validación de titulares duplicados por departamento | OK |
| Paneles admin y consorcista con links | OK |
| CRUD expensas | OK |
| Gastos ordinarios y extraordinarios por proveedor | OK |
| Prorrateo proporcional / igualitario por m2 | OK |
| Validación formato YYYY-MM en período | OK |
| Cálculo automático de expensa por departamento | OK |
| Selector de consorcio y período para generar | OK |
| Vista previa antes de enviar expensas | OK |
| Envío de expensas a consorcistas | OK |
| Mis expensas (consorcista) | OK |
| Historial de pagos con fecha, monto y nota | OK |
| Informar pago | OK |
| Histórico de titularidad por departamento | OK |
| Módulo de reclamos con estados | OK |
| Actualizar estado de reclamos (admin) | OK |
| Módulo de avisos (admin crea, consorcista ve) | OK |
| Desactivar avisos | OK |
| Diseño con Tailwind CSS en todos los templates | OK |
| CRUD Proveedores (vistas custom, sin Django Admin) | OK |
| CRUD Gastos del consorcio (vistas custom, sin Django Admin) | OK |
| CRUD Consorcios (vistas custom, sin Django Admin) | OK |
| CRUD Departamentos (vistas custom, sin Django Admin) | OK |
| CRUD Titularidades (vistas custom, sin Django Admin) | OK |
| CRUD Usuarios (vistas custom, sin Django Admin) | OK |
| CRUD Perfiles (vistas custom, sin Django Admin) | OK |

## Apps del proyecto
- core/        -> home, PanelAdminView, PanelConsorcistView
- consorcios/  -> Consorcio, Departamento, Titularidad, SolicitudVinculacion
- expensas/    -> Proveedor, GastoConsorcio, Expensa, Pago
- usuarios/    -> Perfil, RolRequeridoMixin, redirigir_segun_rol, registro
- reclamos/    -> Reclamo
- avisos/      -> Aviso

## Estructura de selectors

- consorcios/selectors.py -> get_departamento_por_usuario, get_titularidad_activa,
                             get_departamento_por_titularidad, get_titular_en_periodo,
                             get_solicitud_por_usuario, get_todas_las_solicitudes,
                             get_solicitudes_pendientes,
                             get_titularidad_activa_por_departamento,
                             get_titularidades_activas_por_departamento,
                             get_todos_los_consorcios, get_todos_los_departamentos,
                             get_todas_las_titularidades
- expensas/selectors.py   -> get_todas_las_expensas, get_expensas_por_departamento,
                             get_expensa_por_id, get_gastos_por_consorcio_periodo,
                             calcular_monto_departamento, generar_preview_periodo,
                             get_resumen_gastos_periodo, get_pagos_por_expensa,
                             get_todos_los_proveedores, get_todos_los_gastos
- usuarios/selectors.py   -> get_perfil_por_usuario, get_todos_los_perfiles,
                             get_todos_los_usuarios
- reclamos/selectors.py   -> get_reclamos_por_usuario, get_todos_los_reclamos,
                             get_reclamo_por_id
- avisos/selectors.py     -> get_avisos_activos_por_consorcio,
                             get_todos_los_avisos_por_consorcio, get_todos_los_avisos

## URLs disponibles

```
/                                          -> home
/registro/                                 -> registro de usuarios
/redirigir/                                -> redirect segun rol
/panel-admin/                              -> PanelAdminView
/panel-consorcista/                        -> PanelConsorcistView
/mis-expensas/                             -> MisExpensasView
/informar-pago/<id>/                       -> informar_pago
/solicitud/                                -> CrearSolicitudView
/solicitudes/                              -> ListarSolicitudesView
/solicitudes/<id>/                         -> gestionar_solicitud
/solicitudes/retirar/<id>/                 -> retirar_permisos
/listar-expensas/                          -> ListarExpensasView
/expensa/<id>/                             -> DetalleExpensaView
/crear-expensa/                            -> CrearExpensaView
/editar-expensa/<id>/                      -> EditarExpensaView
/eliminar-expensa/<id>/                    -> EliminarExpensaView
/generar-expensas/                         -> SeleccionarPreviewView
/preview/<consorcio_id>/<periodo>/         -> PreviewPeriodoView
/enviar-expensas/<consorcio_id>/<periodo>/ -> enviar_expensas
/mis-reclamos/                             -> MisReclamosView
/crear-reclamo/                            -> CrearReclamoView
/reclamos/                                 -> ListarReclamosView
/reclamos/actualizar/<id>/                 -> actualizar_estado
/avisos/                                   -> ListarAvisosAdminView
/avisos/nuevo/                             -> CrearAvisoView
/avisos/editar/<id>/                       -> EditarAvisoView
/mis-avisos/                               -> MisAvisosView
/proveedores/                              -> ListarProveedoresView
/proveedores/nuevo/                        -> CrearProveedorView
/proveedores/editar/<id>/                  -> EditarProveedorView
/proveedores/eliminar/<id>/                -> EliminarProveedorView
/gastos/                                   -> ListarGastosView
/gastos/nuevo/                             -> CrearGastoView
/gastos/editar/<id>/                       -> EditarGastoView
/gastos/eliminar/<id>/                     -> EliminarGastoView
/consorcios/                               -> ListarConsorciosView
/consorcios/nuevo/                         -> CrearConsorcioView
/consorcios/editar/<id>/                   -> EditarConsorcioView
/consorcios/eliminar/<id>/                 -> EliminarConsorcioView
/departamentos/                            -> ListarDepartamentosView
/departamentos/nuevo/                      -> CrearDepartamentoView
/departamentos/editar/<id>/                -> EditarDepartamentoView
/departamentos/eliminar/<id>/              -> EliminarDepartamentoView
/titularidades/                            -> ListarTitularidadesView
/titularidades/nuevo/                      -> CrearTitularidadView
/titularidades/editar/<id>/                -> EditarTitularidadView
/titularidades/eliminar/<id>/              -> EliminarTitularidadView
/perfiles/                                 -> ListarPerfilesView
/perfiles/nuevo/                           -> CrearPerfilView
/perfiles/editar/<id>/                     -> EditarPerfilView
/perfiles/eliminar/<id>/                   -> EliminarPerfilView
/usuarios/                                 -> ListarUsuariosView
/usuarios/nuevo/                           -> CrearUsuarioView
/usuarios/editar/<id>/                     -> EditarUsuarioView
/usuarios/eliminar/<id>/                   -> EliminarUsuarioView
```

## Pendientes
- [ ] Página separada de confirmación para conflicto de titulares (UX mejorada)

## Mejoras futuras
- [ ] Dashboard con métricas reales en el panel admin
- [ ] Notificaciones por email
- [ ] Paginación y filtros en listados
- [ ] API REST con Django REST Framework
- [ ] Tests automatizados
