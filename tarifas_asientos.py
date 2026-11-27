def calcular_tarifa(tarifa_base: float, pos_origen: int, pos_destino: int) -> float:
    # Hay 5 tramos entre Concepcion (0) y Santiago (5).
    # Por cada tramo que el pasajero no usa, se descuenta un 10% de la tarifa base.
    tramos_totales = 5
    tramos_usados = abs(pos_destino - pos_origen)
    tramos_no_usados = tramos_totales - tramos_usados
    descuento = tarifa_base * 0.10 * tramos_no_usados
    precio = tarifa_base - descuento
    if precio < 0:
        precio = 0.0
    return round(precio, 2)


def orden_tramo(pos_a: int, pos_b: int) -> tuple[int, int]:
    # Deja siempre el numero menor primero y el mayor segundo para comparar tramos.
    if pos_a < pos_b:
        return (pos_a, pos_b)
    return (pos_b, pos_a)


def tramos_chocan(ini_1: int, fin_1: int, ini_2: int, fin_2: int) -> bool:
    # Dos tramos chocan si comparten algun trayecto entre ciudades.
    # Si uno baja en Chillan (1) y el otro sube en Chillan (1), no chocan.
    return ini_1 < fin_2 and ini_2 < fin_1


def asiento_libre(
    pasajes: list[dict[str, str]],
    ciudades_map: dict[str, dict[str, str]],
    id_viaje: str,
    asiento: int,
    pos_origen_nuevo: int,
    pos_destino_nuevo: int,
) -> bool:
    ini_nuevo, fin_nuevo = orden_tramo(pos_origen_nuevo, pos_destino_nuevo)

    for p in pasajes:
        # Solo revisamos pasajes vigentes del mismo viaje y mismo asiento.
        if p["id_viaje"] != id_viaje:
            continue
        if p["estado"] != "VIGENTE":
            continue
        if int(p["asiento"]) != asiento:
            continue

        pos_ori_ex = int(ciudades_map[p["id_origen"]]["posicion"])
        pos_des_ex = int(ciudades_map[p["id_destino"]]["posicion"])
        ini_ex, fin_ex = orden_tramo(pos_ori_ex, pos_des_ex)

        if tramos_chocan(ini_nuevo, fin_nuevo, ini_ex, fin_ex):
            return False

    return True
