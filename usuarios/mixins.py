from django.shortcuts import render


class RolRequeridoMixin:
    rol_requerido = None

    def dispatch(self, request, *args, **kwargs):
        from usuarios.selectors import get_perfil_por_usuario
        perfil = get_perfil_por_usuario(request.user)
        if perfil is None:
            return render(request, 'sin_perfil.html')
        if self.rol_requerido and perfil.rol != self.rol_requerido:
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)
