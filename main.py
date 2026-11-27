from colorama import Fore, Style, init
from catalogos import buscar_secuencial, mapa_ciudades, programar_viaje, registrar_bus, registrar_cliente
from datos import leer_csv, preparar_csv
from interfaz import mostrar_error, mostrar_menu
from pasajes_nomina import anular_pasaje, bubble_sort_nomina, obtener_nomina, vender_pasaje
from tarifas_asientos import asiento_libre


def pedir_entero(mensaje: str) -> int | None:
    try:
        return int(input(mensaje).strip())
    except ValueError:
        mostrar_error("Debes ingresar un numero entero.")
        return None


def pedir_numero(mensaje: str) -> float | None:
    try:
        return float(input(mensaje).strip().replace(",", "."))
    except ValueError:
        mostrar_error("Debes ingresar un numero valido.")
        return None


def ver_nomina() -> None:
    id_viaje = input("ID del viaje (ej. VIA-1): ").strip().upper()
    filas = obtener_nomina(id_viaje)
    if len(filas) == 0:
        print("No hay pasajes vigentes para ese viaje.")
        return

    print("Ordenar por: 1 = Apellido paterno | 2 = Nombres | 3 = Asiento")
    op = input("Opcion: ").strip()
    criterio = "asiento"
    if op == "1":
        criterio = "apellido"
    elif op == "2":
        criterio = "nombre"

    ordenadas = bubble_sort_nomina(filas, criterio)
    print("\n--- NOMINA ---")
    for f in ordenadas:
        print(f"Asiento {f['asiento']} | {f['apellido_paterno']} {f['apellido_materno']}, {f['nombres']} | {f['origen']} -> {f['destino']}")


def ver_reportes() -> None:
    print("\n1. Ver viajes")
    print("2. Ver pasajes y recaudacion de un viaje")
    print("3. Ver asientos libres en un tramo")
    op = input("Opcion: ").strip()

    if op == "1":
        for v in leer_csv("viajes.csv"):
            print(f"{v['id_viaje']} | Bus: {v['id_bus']} | {v['fecha']} {v['hora']} | {v['id_origen']} -> {v['id_destino']} | Base: ${v['tarifa_base']}")
    elif op == "2":
        id_viaje = input("ID del viaje: ").strip().upper()
        total = 0.0
        for p in leer_csv("pasajes.csv"):
            if p["id_viaje"] == id_viaje:
                color = Fore.GREEN if p["estado"] == "VIGENTE" else Fore.RED
                print(f"{p['id_pasaje']} | Asiento {p['asiento']} | {p['id_origen']}->{p['id_destino']} | ${p['valor']} | " + color + p["estado"] + Style.RESET_ALL)
                if p["estado"] == "VIGENTE":
                    total += float(p["valor"])
        print(f"Total recaudado (vigentes): ${total}")
    elif op == "3":
        id_viaje = input("ID del viaje: ").strip().upper()
        ori = input("Ciudad origen (ej. CIU-0): ").strip().upper()
        des = input("Ciudad destino (ej. CIU-2): ").strip().upper()
        viajes = leer_csv("viajes.csv")
        buses = leer_csv("buses.csv")
        pasajes = leer_csv("pasajes.csv")
        _, mapa = mapa_ciudades()

        viaje = buscar_secuencial(viajes, "id_viaje", id_viaje)
        if viaje is None or ori not in mapa or des not in mapa:
            mostrar_error("Datos invalidos.")
            return
        bus = buscar_secuencial(buses, "id_bus", viaje["id_bus"])
        if bus is None:
            mostrar_error("Bus no encontrado.")
            return

        cap = int(bus["capacidad"])
        p_ori = int(mapa[ori]["posicion"])
        p_des = int(mapa[des]["posicion"])
        libres: list[str] = []

        for num in range(1, cap + 1):
            if asiento_libre(pasajes, mapa, viaje["id_viaje"], num, p_ori, p_des):
                libres.append(str(num))

        print("Asientos libres:", ", ".join(libres) if libres else "Ninguno")
    else:
        mostrar_error("Opcion no valida.")


def main() -> None:
    init(autoreset=True)
    preparar_csv()

    while True:
        mostrar_menu()
        op = input("Elige una opcion: ").strip()

        if op == "1":
            registrar_cliente(
                input("RUT: "),
                input("Nombres: "),
                input("Apellido paterno: "),
                input("Apellido materno: "),
                input("Contacto: "),
            )
        elif op == "2":
            clientes = leer_csv("clientes.csv")
            for c in clientes:
                print(f"{c['id_cliente']} | {c['rut']} | {c['apellido_paterno']} {c['apellido_materno']}, {c['nombres']} | {c['contacto']}")
            rut_buscado = input("Buscar RUT (Enter para saltar): ").strip()
            if rut_buscado:
                encontrado = buscar_secuencial(clientes, "rut", rut_buscado)
                print("Encontrado:", encontrado if encontrado else "No existe.")
        elif op == "3":
            sub = input("1 = Registrar bus | 2 = Listar buses: ").strip()
            if sub == "1":
                pat = input("Patente: ")
                cap = pedir_entero("Capacidad: ")
                if cap is not None:
                    registrar_bus(pat, cap)
            else:
                for b in leer_csv("buses.csv"):
                    print(f"{b['id_bus']} | {b['patente']} | Capacidad: {b['capacidad']} | {b['estado']}")
        elif op == "4":
            ciudades, _ = mapa_ciudades()
            for c in ciudades:
                print(f"Posicion {c['posicion']}: {c['nombre']} ({c['id_ciudad']})")
        elif op == "5":
            sub = input("1 = Programar viaje | 2 = Listar viajes: ").strip()
            if sub == "1":
                registrar_viaje_bus = input("ID Bus (ej. BUS-1): ")
                fecha = input("Fecha (ej. 2026-12-01): ")
                hora = input("Hora (ej. 08:30): ")
                ori = input("Origen (CIU-0 o CIU-5): ")
                des = input("Destino (CIU-5 o CIU-0): ")
                tarifa = pedir_numero("Tarifa base: ")
                if tarifa is not None:
                    programar_viaje(registrar_viaje_bus, fecha, hora, ori, des, tarifa)
            else:
                for v in leer_csv("viajes.csv"):
                    print(f"{v['id_viaje']} | Bus: {v['id_bus']} | {v['fecha']} {v['hora']} | {v['id_origen']} -> {v['id_destino']} | Base: ${v['tarifa_base']}")
        elif op == "6":
            id_cli = input("ID Cliente (ej. CLI-1): ")
            id_via = input("ID Viaje (ej. VIA-1): ")
            ori = input("Origen pasajero (ej. CIU-0): ")
            des = input("Destino pasajero (ej. CIU-1): ")
            asiento = pedir_entero("Numero de asiento: ")
            if asiento is not None:
                vender_pasaje(id_cli, id_via, ori, des, asiento)
        elif op == "7":
            anular_pasaje(input("ID Pasaje a anular (ej. PAS-1): "))
        elif op == "8":
            ver_nomina()
        elif op == "9":
            ver_reportes()
        elif op == "0":
            print("Saliendo del sistema...")
            break
        else:
            mostrar_error("Opcion no valida.")


if __name__ == "__main__":
    main()
