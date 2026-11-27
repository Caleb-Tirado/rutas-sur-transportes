import csv
import os
from colorama import Fore, Style

ARCHIVOS: dict[str, list[str]] = {
    "clientes.csv": ["id_cliente", "rut", "nombres", "apellido_paterno", "apellido_materno", "contacto"],
    "buses.csv": ["id_bus", "patente", "capacidad", "estado"],
    "ciudades.csv": ["id_ciudad", "nombre", "posicion"],
    "viajes.csv": ["id_viaje", "id_bus", "fecha", "hora", "id_origen", "id_destino", "tarifa_base"],
    "pasajes.csv": ["id_pasaje", "id_viaje", "id_cliente", "id_origen", "id_destino", "asiento", "valor", "estado"],
}

CIUDADES_INICIALES: list[dict[str, str]] = [
    {"id_ciudad": "CIU-0", "nombre": "Concepcion", "posicion": "0"},
    {"id_ciudad": "CIU-1", "nombre": "Chillan", "posicion": "1"},
    {"id_ciudad": "CIU-2", "nombre": "Linares", "posicion": "2"},
    {"id_ciudad": "CIU-3", "nombre": "Talca", "posicion": "3"},
    {"id_ciudad": "CIU-4", "nombre": "Rancagua", "posicion": "4"},
    {"id_ciudad": "CIU-5", "nombre": "Santiago", "posicion": "5"},
]


def preparar_csv() -> None:
    # Si falta algun CSV o esta vacio, crea los encabezados.
    for nombre, columnas in ARCHIVOS.items():
        try:
            if not os.path.exists(nombre) or os.path.getsize(nombre) == 0:
                with open(nombre, "w", newline="", encoding="utf-8") as f:
                    escritor = csv.DictWriter(f, fieldnames=columnas)
                    escritor.writeheader()
                    if nombre == "ciudades.csv":
                        escritor.writerows(CIUDADES_INICIALES)
        except OSError as e:
            print(Fore.RED + f"Error al crear {nombre}: {e}" + Style.RESET_ALL)


def leer_csv(nombre: str) -> list[dict[str, str]]:
    # Lee el CSV y devuelve una lista de diccionarios (cada fila es un diccionario).
    preparar_csv()
    filas: list[dict[str, str]] = []
    try:
        with open(nombre, "r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                filas.append(dict(fila))
    except OSError as e:
        print(Fore.RED + f"Error al leer {nombre}: {e}" + Style.RESET_ALL)
    return filas


def guardar_csv(nombre: str, filas: list[dict[str, str]]) -> bool:
    # Sobrescribe el CSV con la lista completa actualizada.
    columnas = ARCHIVOS[nombre]
    try:
        with open(nombre, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas)
        return True
    except OSError as e:
        print(Fore.RED + f"Error al guardar {nombre}: {e}" + Style.RESET_ALL)
        return False
