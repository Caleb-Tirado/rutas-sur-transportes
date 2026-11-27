from datos import guardar_csv, leer_csv
from interfaz import mostrar_error, mostrar_exito


def buscar_secuencial(lista: list[dict[str, str]], campo: str, buscado: str) -> dict[str, str] | None:
    # Recorre la lista uno por uno hasta encontrar el dato.
    for item in lista:
        if item[campo].strip().lower() == buscado.strip().lower():
            return item
    return None


def siguiente_id(lista: list[dict[str, str]], campo_id: str, prefijo: str) -> str:
    # Toma el numero mas alto que exista y le suma 1.
    mayor = 0
    for item in lista:
        partes = item[campo_id].split("-")
        if len(partes) == 2 and partes[1].isdigit():
            num = int(partes[1])
            if num > mayor:
                mayor = num
    return f"{prefijo}-{mayor + 1}"


def mapa_ciudades() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    ciudades = leer_csv("ciudades.csv")
    mapa: dict[str, dict[str, str]] = {}
    for c in ciudades:
        mapa[c["id_ciudad"]] = c
    return ciudades, mapa


def registrar_cliente(rut: str, nombres: str, ap_pat: str, ap_mat: str, contacto: str) -> None:
    if not rut.strip() or not nombres.strip() or not ap_pat.strip():
        mostrar_error("Faltan datos obligatorios del cliente.")
        return

    clientes = leer_csv("clientes.csv")
    if buscar_secuencial(clientes, "rut", rut) is not None:
        mostrar_error("Ese RUT ya esta registrado.")
        return

    nuevo = {
        "id_cliente": siguiente_id(clientes, "id_cliente", "CLI"),
        "rut": rut.strip(),
        "nombres": nombres.strip(),
        "apellido_paterno": ap_pat.strip(),
        "apellido_materno": ap_mat.strip(),
        "contacto": contacto.strip(),
    }
    clientes.append(nuevo)
    if guardar_csv("clientes.csv", clientes):
        mostrar_exito(f"Cliente guardado con ID {nuevo['id_cliente']}.")


def registrar_bus(patente: str, capacidad: int) -> None:
    if not patente.strip() or capacidad <= 0:
        mostrar_error("Patente invalida o capacidad menor a 1.")
        return

    buses = leer_csv("buses.csv")
    if buscar_secuencial(buses, "patente", patente) is not None:
        mostrar_error("Esa patente ya existe.")
        return

    nuevo = {
        "id_bus": siguiente_id(buses, "id_bus", "BUS"),
        "patente": patente.strip().upper(),
        "capacidad": str(capacidad),
        "estado": "DISPONIBLE",
    }
    buses.append(nuevo)
    if guardar_csv("buses.csv", buses):
        mostrar_exito(f"Bus guardado con ID {nuevo['id_bus']}.")


def programar_viaje(id_bus: str, fecha: str, hora: str, origen: str, destino: str, tarifa_base: float) -> None:
    buses = leer_csv("buses.csv")
    viajes = leer_csv("viajes.csv")
    _, mapa = mapa_ciudades()

    bus = buscar_secuencial(buses, "id_bus", id_bus)
    if bus is None:
        mostrar_error("No existe ese bus.")
        return
    if bus["estado"] != "DISPONIBLE":
        mostrar_error("El bus no esta disponible.")
        return

    origen = origen.strip().upper()
    destino = destino.strip().upper()
    if origen not in mapa or destino not in mapa:
        mostrar_error("Ciudad de origen o destino invalida.")
        return

    # Solo viajes entre Concepcion (CIU-0) y Santiago (CIU-5).
    if not ((origen == "CIU-0" and destino == "CIU-5") or (origen == "CIU-5" and destino == "CIU-0")):
        mostrar_error("El viaje debe ser entre Concepcion y Santiago.")
        return

    nuevo = {
        "id_viaje": siguiente_id(viajes, "id_viaje", "VIA"),
        "id_bus": bus["id_bus"],
        "fecha": fecha.strip(),
        "hora": hora.strip(),
        "id_origen": origen,
        "id_destino": destino,
        "tarifa_base": str(tarifa_base),
    }
    viajes.append(nuevo)
    if guardar_csv("viajes.csv", viajes):
        mostrar_exito(f"Viaje guardado con ID {nuevo['id_viaje']}.")
