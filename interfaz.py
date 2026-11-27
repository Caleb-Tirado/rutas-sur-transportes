from colorama import Fore, Style


def mostrar_exito(texto: str) -> None:
    print(Fore.GREEN + "[OK] " + texto + Style.RESET_ALL)


def mostrar_error(texto: str) -> None:
    print(Fore.RED + "[ERROR] " + texto + Style.RESET_ALL)


def mostrar_menu() -> None:
    print(Fore.CYAN + "\n=== RUTASUR TRANSPORTES ===" + Style.RESET_ALL)
    print("1. Registrar cliente")
    print("2. Listar y buscar clientes")
    print("3. Registrar y listar buses")
    print("4. Ver ciudades")
    print("5. Programar y listar viajes")
    print("6. Vender pasaje")
    print("7. Anular pasaje")
    print("8. Ver nomina ordenada")
    print("9. Reportes y asientos libres")
    print("0. Salir")
