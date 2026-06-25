from decimal import Decimal
from .models import Expensa, GastoConsorcio


def get_todas_las_expensas():
    return Expensa.objects.all()


def get_expensas_por_departamento(departamento):
    return Expensa.objects.filter(
        departamento=departamento,
        publicada=True
    )


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

    # Calcular m2 totales del consorcio
    deptos = consorcio.departamento_set.all()
    m2_totales = sum(d.metros_cuadrados for d in deptos)

    if m2_totales == 0:
        return Decimal('0')

    porcentaje = m2_depto / m2_totales
    total = Decimal('0')

    for gasto in gastos:
        if gasto.tipo == 'ordinario':
            total += gasto.monto * porcentaje

        elif gasto.tipo == 'extraordinario':
            if gasto.alcance == 'general':
                total += gasto.monto * porcentaje

            elif gasto.alcance == 'por_departamento':
                deptos_involucrados = gasto.departamentos.all()
                if departamento not in deptos_involucrados:
                    continue
                if gasto.prorrateo == 'igualitario':
                    cantidad = deptos_involucrados.count()
                    if cantidad > 0:
                        total += gasto.monto / cantidad
                else:
                    m2_involucrados = sum(
                        d.metros_cuadrados for d in deptos_involucrados
                    )
                    if m2_involucrados > 0:
                        total += gasto.monto * (m2_depto / m2_involucrados)

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


def get_pagos_por_expensa(expensa):
    from .models import Pago
    return Pago.objects.filter(expensa=expensa).order_by('-fecha')


def get_todos_los_proveedores():
    from .models import Proveedor
    return Proveedor.objects.all().order_by('nombre')


def get_todos_los_gastos():
    return GastoConsorcio.objects.all().order_by('-periodo')
