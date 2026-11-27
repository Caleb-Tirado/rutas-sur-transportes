# RutaSur Transportes

Sistema de consola en Python para administrar clientes, buses, ciudades, viajes y venta o anulacion de pasajes entre Concepcion y Santiago, pasando por ciudades intermedias.

## Integrantes
- Caleb Tirado
- Joaquin Fuentes

## Instalacion y ejecucion
1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt

## Como esta organizado el proyecto

datos.py: crea o revisa los archivos CSV y se encarga de leerlos y guardarlos.

interfaz.py: muestra el menu y los mensajes con colores usando colorama.

tarifas_asientos.py: calcula el valor del pasaje segun el tramo y revisa si un asiento esta libre o choca con otro tramo ya vendido.

catalogos.py: maneja clientes, buses, ciudades y programacion de viajes.

pasajes_nomina.py: vende pasajes, los anula y arma la nomina de pasajeros de un viaje.

main.py: muestra el menu principal y conecta todas las opciones.

clientes.csv, buses.csv, ciudades.csv, viajes.csv, pasajes.csv: guardan toda la informacion para que no se pierda al cerrar el programa.

## Estructuras de datos y algoritmos utilizados

Busqueda secuencial: recorremos las listas de registros una por una para encontrar clientes, buses, viajes o pasajes, y para revisar que no se repitan datos como el RUT o la patente.

Ordenamiento burbuja (Bubble Sort): lo usamos para ordenar la nomina de pasajeros de un viaje por apellido paterno, nombres o numero de asiento (con criterios extra si hay empate), comparando elementos de a par sin depender de funciones ya listas de ordenamiento.

Pruebas realizadas
Se probo registrar clientes y buses y comprobar que rechace RUT o patentes repetidas.

Se probaron viajes y tramos (por ejemplo Concepcion a Santiago, Chillan a Santiago o tramos mas cortos) para revisar el calculo del precio.

Se probo vender el mismo asiento en tramos que no se cruzan (si deja) y en tramos que si chocan (lo rechaza).

Se probo anular un pasaje para ver que libere solo ese tramo, no cuente en la plata recaudada y no se pueda anular dos veces.

Se cerro y volvio a abrir el programa para confirmar que todo quedo guardado en los CSV.