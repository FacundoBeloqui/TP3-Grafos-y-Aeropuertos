from funciones import camino_minimo, camino_escalas, centralidad, nueva_ruta, itinerario, exportar_kml
import sys

def chequear_parametros(parametros, cant_esperada):
    if len(parametros) != cant_esperada:
        print(f"Error en cantidad de argumentos, deberian ser {cant_esperada}")
        return False
    return True


def procesar_comando(linea, aeropuertos, vuelos, dicc_ciudades, grafo, ultima_salida, centralidad_total):
    comando, params = linea.split(" ", 1)
    parametros = params.split(",")


    if comando == 'camino_mas':
        if not chequear_parametros(parametros, 3):
            return ultima_salida
        
        origen = parametros[1]
        destino = parametros[2]
        if parametros[0] == "rapido":
            return camino_minimo(grafo, dicc_ciudades, origen, destino, lambda vuelo: vuelo.tiempo)
        elif parametros[0] == "barato":
            return camino_minimo(grafo, dicc_ciudades, origen, destino, lambda vuelo: vuelo.precio)

    elif comando ==  'camino_escalas':
        if not chequear_parametros(parametros, 2):
            return ultima_salida
        
        origen = parametros[0]
        destino = parametros[1]
        return camino_escalas(grafo, dicc_ciudades, origen, destino)

    elif comando == 'centralidad':
        if not chequear_parametros(parametros, 1):
            return ultima_salida

        n = int(parametros[0])
        centralidad(grafo, n)

    elif comando == 'nueva_aerolinea':
        if not chequear_parametros(parametros, 1):
            return ultima_salida

        ruta_salida = parametros[0]
        nueva_ruta(grafo, vuelos, ruta_salida)

    elif comando == 'itinerario':
        if not chequear_parametros(parametros, 1):
            return ultima_salida

        ruta = parametros[0]
        itinerario(grafo, dicc_ciudades, ruta)

    elif comando == "exportar_kml":
        if not chequear_parametros(parametros, 1):
            return ultima_salida
        
        ruta_archivo =parametros[0]
        exportar_kml(ultima_salida, aeropuertos, ruta_archivo)

    elif comando == 'salir':
        sys.exit(0)

    else:
        print(f"Comando inválido o parámetros incorrectos: {linea}", file=sys.stderr)