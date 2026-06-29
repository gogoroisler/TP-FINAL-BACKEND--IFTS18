from decimal import Decimal
from .models import Expensa, GastoConsorcio


class _ProporcionConsorcio:
    def calcular(self, gasto, departamento, m2_depto, m2_totales):
        if m2_totales > 0:
            return gasto.monto * (m2_depto / m2_totales)
        return Decimal('0')


class _IgualitarioPorDepartamento:
    def calcular(self, gasto, departamento, m2_depto, m2_totales):
        deptos = gasto.departamentos.all()
        if departamento not in deptos:
            return None
        cantidad = deptos.count()
        return gasto.monto / cantidad if cantidad > 0 else Decimal('0')


class _ProporcionalPorDepartamento:
    def calcular(self, gasto, departamento, m2_depto, m2_totales):
        deptos = gasto.departamentos.all()
        if departamento not in deptos:
            return None
        m2_inv = sum(d.metros_cuadrados for d in deptos)
        return gasto.monto * (m2_depto / m2_inv) if m2_inv > 0 else Decimal('0')


def _estrategia_gasto(gasto):
    if gasto.tipo == 'ordinario' or gasto.alcance == 'general':
        return _ProporcionConsorcio()
    if gasto.prorrateo == 'igualitario':
        return _IgualitarioPorDepartamento()
    return _ProporcionalPorDepartamento()


def get_todas_las_expensas():
    return Expensa.objects.select_related('departamento__consorcio').order_by('-periodo', 'departamento__consorcio__nombre', 'departamento__numero')


def get_expensas_por_departamento(departamento):
    return Expensa.objects.filter(
        departamento=departamento,
        publicada=True
    ).order_by('-periodo')


def get_expensa_por_id(expensa_id):
    return Expensa.objects.get(id=expensa_id)


def get_gastos_por_consorcio_periodo(consorcio, periodo):
    return GastoConsorcio.objects.filter(
        consorcio=consorcio,
        periodo=periodo
    )


def calcular_monto_departamento(departamento, periodo):
    consorcio = departamento.consorcio
    m2_depto = departamento.metros_cuadrados
    gastos = get_gastos_por_consorcio_periodo(consorcio, periodo)
    m2_totales = sum(d.metros_cuadrados for d in consorcio.departamento_set.all())

    if m2_totales == 0:
        return Decimal('0')

    total = Decimal('0')
    for gasto in gastos:
        contribucion = _estrategia_gasto(gasto).calcular(gasto, departamento, m2_depto, m2_totales)
        if contribucion is not None:
            total += contribucion

    return total.quantize(Decimal('0.01'))


def generar_preview_periodo(consorcio, periodo):
    deptos = consorcio.departamento_set.all()
    m2_totales = sum(d.metros_cuadrados for d in deptos)
    gastos = get_gastos_por_consorcio_periodo(consorcio, periodo)
    total_consorcio = sum(g.monto for g in gastos)

    preview = []
    for depto in deptos:
        monto = calcular_monto_departamento(depto, periodo)
        porcentaje = (
            (depto.metros_cuadrados / m2_totales * 100)
            if m2_totales > 0 else 0
        )
        preview.append({
            'departamento': depto,
            'metros_cuadrados': depto.metros_cuadrados,
            'porcentaje': round(porcentaje, 2),
            'monto': monto,
        })

    return {
        'consorcio': consorcio,
        'periodo': periodo,
        'total_consorcio': total_consorcio,
        'detalle': preview,
    }


def get_resumen_gastos_periodo(consorcio, periodo):
    gastos = get_gastos_por_consorcio_periodo(consorcio, periodo)
    total = sum(g.monto for g in gastos)
    return {
        'gastos': gastos,
        'total': total,
    }


def get_detalle_gastos_por_expensa(expensa):
    departamento = expensa.departamento
    consorcio = departamento.consorcio
    m2_depto = departamento.metros_cuadrados
    gastos = get_gastos_por_consorcio_periodo(consorcio, expensa.periodo)
    m2_totales = sum(d.metros_cuadrados for d in consorcio.departamento_set.all())

    detalle = []
    subtotal_ordinario = Decimal('0')
    subtotal_extraordinario = Decimal('0')

    for gasto in gastos:
        contribucion = _estrategia_gasto(gasto).calcular(gasto, departamento, m2_depto, m2_totales)
        if contribucion is None:
            continue
        contribucion = contribucion.quantize(Decimal('0.01'))
        detalle.append({'gasto': gasto, 'contribucion': contribucion})
        if gasto.tipo == 'ordinario':
            subtotal_ordinario += contribucion
        else:
            subtotal_extraordinario += contribucion

    detalle.sort(key=lambda x: 0 if x['gasto'].tipo == 'ordinario' else 1)

    return {
        'detalle': detalle,
        'subtotal_ordinario': subtotal_ordinario,
        'subtotal_extraordinario': subtotal_extraordinario,
        'total_consorcio': sum(g.monto for g in gastos),
    }


def get_pagos_por_expensa(expensa):
    from .models import Pago
    return Pago.objects.filter(expensa=expensa).order_by('-fecha')


def get_todos_los_proveedores():
    from .models import Proveedor
    return Proveedor.objects.all().order_by('nombre')


def get_todos_los_gastos():
    return GastoConsorcio.objects.all().order_by('-periodo')


def get_credito_disponible(departamento):
    expensas = Expensa.objects.filter(
        departamento=departamento,
        publicada=True,
    ).prefetch_related('pagos')
    credito = Decimal('0')
    for expensa in expensas:
        saldo = expensa.saldo_pendiente
        if saldo < 0:
            credito += abs(saldo)
    return credito
