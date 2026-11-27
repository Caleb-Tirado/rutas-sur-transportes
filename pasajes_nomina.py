from catalogos import buscar_secuencial, mapa_ciudades, siguiente_id
from datos import guardar_csv, leer_csv
from interfaz import mostrar_error, mostrar_exito
from tarifas_asientos import asiento_libre, calcular_tarifa


def sentido_valido(pos_viaje_ori: int, pos_viaje_des: int, pos_pas_ori: int, pos_pas_des: int) -> bool:
    if pos_pas_ori == pos_pas_des:
        return False
    # Viaje de sur a norte (0 -> 5): origen del pasajero debe ir antes que destino.
    if pos_viaje_ori < pos_viaje_des:
        return pos_pas_ori < pos_pas_des
    # Viaje de norte a sur (5 -> 0): origen del pasajero debe ir despues que destino.
    return pos_pas_ori > pos_pas_des


def vender_pasaje(id_cliente: str, id_viaje: str, origen: str, destino: str, asiento: int) -> None:
    clientes = leer_csv("clientes.csv")
    viajes = leer_csv("viajes.csv")
    buses = leer_csv("buses.csv")
    pasajes = leer_csv("pasajes.csv")
    _, mapa = mapa_ciudades()

    cliente = buscar_secuencial(clientes, "id_cliente", id_cliente)
    if cliente is None:
        mostrar_error("Cliente no encontrado.")
        return

    viaje = buscar_secuencial(viajes, "id_viaje", id_viaje)
    if viaje is None:
        mostrar_error("Viaje no encontrado.")
        return

    bus = buscar_secuencial(buses, "id_bus", viaje["id_bus"])
    if bus is None:
        mostrar_error("Bus no encontrado.")
        return

    capacidad = int(bus["capacidad"])
    if asiento < 1 or asiento > capacidad:
        mostrar_error(f"El asiento debe estar entre 1 y {capacidad}.")
        return

    origen = origen.strip().upper()
    destino = destino.strip().upper()
    if origen not in mapa or destino not in mapa:
        mostrar_error("Ciudad invalida.")
        return

    pos_v_ori = int(mapa[viaje["id_origen"]]["posicion"])
    pos_v_des = int(mapa[viaje["id_destino"]]["posicion"])
    pos_p_ori = int(mapa[origen]["posicion"])
    pos_p_des = int(mapa[destino]["posicion"])

    if not sentido_valido(pos_v_ori, pos_v_des, pos_p_ori, pos_p_des):
        mostrar_error("El tramo no coincide con el sentido del viaje.")
        return

    libre = asiento_libre(pasajes, mapa, viaje["id_viaje"], asiento, pos_p_ori, pos_p_des)
    if not libre:
        mostrar_error("Ese asiento ya esta ocupado en ese tramo.")
        return

    tarifa_base = float(viaje["tarifa_base"])
    valor = calcular_tarifa(tarifa_base, pos_p_ori, pos_p_des)

    nuevo = {
        "id_pasaje": siguiente_id(pasajes, "id_pasaje", "PAS"),
        "id_viaje": viaje["id_viaje"],
        "id_cliente": cliente["id_cliente"],
        "id_origen": origen,
        "id_destino": destino,
        "asiento": str(asiento),
        "valor": str(valor),
        "estado": "VIGENTE",
    }
    pasajes.append(nuevo)
    if guardar_csv("pasajes.csv", pasajes):
        mostrar_exito(f"Pasaje {nuevo['id_pasaje']} vendido por ${valor}.")


def anular_pasaje(id_pasaje: str) -> None:
    pasajes = leer_csv("pasajes.csv")
    for p in pasajes:
        if p["id_pasaje"].strip().upper() == id_pasaje.strip().upper():
            if p["estado"] == "ANULADO":
                mostrar_error("El pasaje ya estaba anulado.")
                return
            p["estado"] = "ANULADO"
            if guardar_csv("pasajes.csv", pasajes):
                mostrar_exito(f"Pasaje {p['id_pasaje']} anulado.")
            return
    mostrar_error("No se encontro ese pasaje.")


def obtener_nomina(id_viaje: str) -> list[dict[str, str]]:
    pasajes = leer_csv("pasajes.csv")
    clientes = leer_csv("clientes.csv")
    _, mapa = mapa_ciudades()

    lista: list[dict[str, str]] = []
    for p in pasajes:
        if p["id_viaje"].strip().upper() == id_viaje.strip().upper() and p["estado"] == "VIGENTE":
            cli = buscar_secuencial(clientes, "id_cliente", p["id_cliente"])
            if cli is not None:
                lista.append({
                    "id_pasaje": p["id_pasaje"],
                    "asiento": p["asiento"],
                    "apellido_paterno": cli["apellido_paterno"],
                    "apellido_materno": cli["apellido_materno"],
                    "nombres": cli["nombres"],
                    "origen": mapa[p["id_origen"]]["nombre"],
                    "destino": mapa[p["id_destino"]]["nombre"],
                    "valor": p["valor"],
                })
    return lista


def bubble_sort_nomina(filas: list[dict[str, str]], criterio: str) -> list[dict[str, str]]:
    # Algoritmo Bubble Sort hecho a mano: compara vecinos y los intercambia si estan desordenados.
    datos = list(filas)
    n = len(datos)
    for i in range(n):
        for j in range(0, n - i - 1):
            a = datos[j]
            b = datos[j + 1]
            cambiar = False

            if criterio == "apellido":
                if a["apellido_paterno"].lower() > b["apellido_paterno"].lower():
                    cambiar = True
                elif a["apellido_paterno"].lower() == b["apellido_paterno"].lower():
                    if a["nombres"].lower() > b["nombres"].lower():
                        cambiar = True
            elif criterio == "nombre":
                if a["nombres"].lower() > b["nombres"].lower():
                    cambiar = True
                elif a["nombres"].lower() == b["nombres"].lower():
                    if a["apellido_paterno"].lower() > b["apellido_paterno"].lower():
                        cambiar = True
            else:
                if int(a["asiento"]) > int(b["asiento"]):
                    cambiar = True

            if cambiar:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
    return datos
