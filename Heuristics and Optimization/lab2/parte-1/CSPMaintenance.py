from constraint import *
import sys
import csv


# primero necesitaremos una función que lea los datos de entrada
def leer_entrada(archivo):
    # Debemos leer el fichero por líneas, asumimos que está en formato correcto
    """
    1ª línea: franjas horarias del problema
    2ª línea: tamaño de la matriz de talleres
    3ª línea: posiciones de los talleres estándar
    4ª línea: posiciones de los talleres especialistas
    5ª línea: posiciones de los parkings
    6ª y posteriores: código de identificación de los aviones ID-TIPO-RESTR-T1-T2
    """
    with open(archivo, 'r') as f:
        linea = f.readlines()  # aquí podemos identificar en que línea estamos

    n_franjas_horarias = int(linea[0].strip(".Franjas: "))  # guarda solo el número de esa primera línea
    matriz_size = list(map(int, linea[1].split("x")))

    # split generaria una lista de str, con map los pasamos a int para guardar el tamaño de la matriz nxm
    coordenadas_std = linea[2].strip(".STD:").split(" ")
    # se guarda como elementos str "(x,y)", y queremos un tuple de listas de dos números
    talleres_std = []
    for elem in coordenadas_std:
        elem_sin_parentesis = elem.strip("()\n")
        x, y = elem_sin_parentesis.split(",")
        talleres_std.append((int(x), int(y)))

    # hacemos lo mismo para sacar los talleres SPC y los PRK:
    coordenadas_spc = linea[3].strip(".SPC:").split(" ")
    talleres_spc = []
    for elem in coordenadas_spc:
        elem_sin_parentesis = elem.strip("()\n")
        x, y = elem_sin_parentesis.split(",")
        talleres_spc.append((int(x), int(y)))

    coordenadas_prk = linea[4].strip(".PRK:").split(" ")
    prk = []
    for elem in coordenadas_prk:
        elem_sin_parentesis = elem.strip("()\n")
        x, y = elem_sin_parentesis.split(",")
        prk.append((int(x), int(y)))

    # Por último, guardo los aviones en una lista de diccionarios para cada avión con:
    # {id: , tipo: , restriccion: bool, T1: , T2: }
    aviones = []
    for i in linea[5:]:  # ya es desde la 5ª línea hasta el final
        partes = i.strip().split("-")
        aviones.append((
            {
                'id': int(partes[0]),
                'tipo': partes[1],
                'restriccion': partes[2] == 'T',  # Si es igual a T da True, si no False
                'T1': int(partes[3]),
                'T2': int(partes[4]),
            }
        ))

    # Por último, comprobamos que el tamaño de la matriz coincida con todos los talleres y parkings
    posiciones = talleres_std + talleres_spc + prk
    total_matriz = matriz_size[0] * matriz_size[1]
    if total_matriz != len(posiciones):
        raise ValueError("Error: El tamaño de la matriz y el número de posiciones no coincide")

    return n_franjas_horarias, matriz_size, talleres_std, talleres_spc, prk, aviones


# HACER FUNCION PARA DEVOLVER EL RESULTADO EN UN ARCHIVO NUEVO!!!!!------------------------------------------
def generar_resultado(archivo_salida, soluciones, aviones, n_franjas_horarias, posiciones):
    with open(archivo_salida, 'w', newline='') as f:
        f.write(f"N. Sol: {len(soluciones)}\n")  # Número total de soluciones encontradas

        for i, solucion in enumerate(soluciones, start=1):
            f.write(f"Solución {i}:\n")  # Encabezado de la solución
            for avion in aviones:
                asignaciones = []
                for franja in range(n_franjas_horarias):
                    posicion = solucion.get((avion["id"], franja))
                    # Buscar el tipo de posición en la lista `posiciones`
                    tipo_posicion = next((p[0] for p in posiciones if p[1] == posicion), "UNK")
                    asignaciones.append(f"{tipo_posicion}{posicion}")

                # Escribir la línea del avión con asignaciones
                f.write(
                    f"{avion['id']}-{avion['tipo']}-{'T' if avion['restriccion'] else 'F'}-{avion['T1']}-{avion['T2']}: ")
                f.write(", ".join(asignaciones) + "\n")

            f.write("\n")  # Espacio entre soluciones


def modelar_problema(n_franjas_horarias, matriz_size, talleres_std, talleres_spc, prk, aviones):
    problema = Problem()
    posiciones = talleres_std + talleres_spc + prk

    # Creamos las variables. Basándonos en nuestro modelo, todos los aviones en cada franja horaria
    for avion in aviones:
        for franja in range(n_franjas_horarias):
            problema.addVariable((avion["id"], franja), posiciones)
            # una variable para cada avion y para cada franja horaria, dentro del dominio de todas las posiciones

    """
    R1: Todos los aviones asignados a un taller/parking
    """
    for avion in aviones:
        problema.addConstraint(
            lambda *asignaciones: all(posicion is not None for posicion in asignaciones),
            [(avion['id'], franja) for franja in range(n_franjas_horarias)]
        )
    # sacamos una lista de que aviones se habrían asignado en esa franja de tiempo.
    # *asignaciones = [(id_avion, franja_horaria), ...]
    # lambda es una mini funcion sin necesidad de usar def
    # *asignaciones multiples argumentos empaquetados como tuple
    # la funcion itera sobre todas las posiciones dadas en la lista, devolviendo Trie si no hay ninguna vacía

    # solo usando la variable R1, se genera un fichero enorme con todas las combinaciones de celdas posibles

    """
    R2: Máximo por posición 2 STD o 1 JMB
    """
    for franja in range(n_franjas_horarias):
        # DEBUG
        print(f"Procesando franja horaria {franja}")
        problema.addConstraint(
            lambda *asignaciones: validar_aviones_posicion(asignaciones, aviones, posiciones),
            [(avion['id'], franja) for avion in aviones]
        )

    """
    R3: Talleres SPC -> t1, t2 ; Talleres STD -> t1
    """
    # Comprobar quen los que tengan tareas t2 pasen por talleres SPC
    for avion in aviones:
        if avion["T2"] > 0:  # Tiene tareas T2 (SPC)
            # print(f"Avión {avion['id']} tiene tareas T2 ({avion['T2']}), verificando talleres SPC...")
            problema.addConstraint(
                lambda *asignaciones, avion_actual=avion: verificar_taller_t2(asignaciones, avion_actual, talleres_spc,
                                                                              talleres_std),
                [(avion['id'], franja) for franja in range(n_franjas_horarias)]  # Todas las franjas para este avión
            )
        elif avion["T1"] > 0:  # No hay T2, pero sí T1
            # print(f"Avión {avion['id']} tiene tareas T1 ({avion['T1']}), verificando talleres STD/SPC...")
            problema.addConstraint(
                lambda *asignaciones, avion_actual=avion: verificar_t1(asignaciones, avion_actual, talleres_spc,
                                                                       talleres_std),
                [(avion['id'], franja) for franja in range(n_franjas_horarias)]  # Todas las franjas para este avión
            )

            # else: no hay tareas, da igual donde coloquemos el avion

    """
    R4: Si 'restriccion' = True, todas las tareas t2 se deben completar antes que las t1
    """
    for avion in aviones:
        if avion["restriccion"]:  # restriccion == True
            problema.addConstraint(
                lambda *asignaciones, avion_actual=avion: verificar_orden_tareas(asignaciones, avion_actual),
                [(avion['id'], franja) for franja in range(n_franjas_horarias)]
                # Variables de este avión en todas las franjas
            )

    """
    R5: Si hay un avión, al menos una casilla adyacente debe estar vacía
    """
    for franja in range(n_franjas_horarias):
        # Añadimos la restricción para la franja horaria actual
        problema.addConstraint(
            lambda *asignaciones: verificar_r5(asignaciones, talleres_std, talleres_spc, prk),
            [(avion['id'], franja) for avion in aviones]  # Pasamos el ID del avión y la franja como variables
        )

    """
    R6: Dos JMB no pueden estar en posiciones adyacentes
    """
    for franja in range(n_franjas_horarias):
        problema.addConstraint(
            lambda *asignaciones, franja_actual=franja: verificar_r6(asignaciones, talleres_std, talleres_spc, prk,
                                                                     aviones, franja_actual),
            [(avion['id'], franja) for avion in aviones if avion['tipo'] == 'JMB']
        )

    return problema


# ##################################### FUNCIONES EXTERNAS PARA LA MODELIZACIÓN #####################################
def validar_aviones_posicion(asignaciones, aviones, posiciones):
    # el "posiciones" recibido es una lista con todas las posiciones disponibles en nuestro problema
    # como lo llamamos desde fuera, ya se hace franja por franja no es necesario volver a ponerlo aqui
    posiciones_por_franja = {pos: [] for pos in posiciones}
    # genera un diccionario con la estructura {(0, 0): [],(1, 1): [],(0, 1): [],(1, 0): []} (para una 2x2)

    for avion, posicion in zip(aviones, asignaciones):
        if posicion in posiciones_por_franja:
            posiciones_por_franja[posicion].append(avion["tipo"])

    # Ahora revisamos las restricciones sobre los tipos de aviones en cada posición
    for posicion, tipos in posiciones_por_franja.items():
        # Si hay más de 2 aviones o si hay más de 1 "JMB", descartar la asignación
        if len(tipos) > 2:
            return False

        if "JMB" in tipos and len(tipos) != 1:
            return False

    # Si todas las restricciones son wenas
    return True


def verificar_taller_t2(asignaciones, avion, talleres_spc, talleres_std):
    # for avion in aviones se hace fuera, al comienzo de R·
    tareas_t1 = avion["T1"]
    tareas_t2 = avion["T2"]

    n_veces_spc = 0  # contador para cuantas veces pasa el avion por un taller spc
    n_veces_std = 0

    # Verificar cuántas veces el avión es asignado a un taller SPC
    for asignacion in asignaciones:
        if asignacion in talleres_spc:
            n_veces_spc += 1
        elif asignacion in talleres_std:
            n_veces_std += 1

    # Verificar que el avión pasa por suficientes talleres SPC
    if n_veces_spc >= tareas_t2:
        # Verificar que el número total de talleres asignados (SPC + STD) cubra todas las tareas
        if n_veces_std + n_veces_spc >= (tareas_t1 + tareas_t2):
            return True

    return False


def verificar_t1(asignaciones, avion, talleres_spc, talleres_std):
    total_talleres = talleres_std + talleres_spc
    talleres_necesarios = avion["T1"]
    talleres_por_los_que_paso = 0  # flag para comparar al final

    for asignacion in asignaciones:
        if asignacion in total_talleres:  # si la posicion esta en total_talleres
            talleres_por_los_que_paso += 1

    if talleres_por_los_que_paso >= talleres_necesarios:
        return True

    return False


def verificar_orden_tareas(asignaciones, avion):
    # Obtener las franjas horarias asignadas al avión
    franjas_asignadas = [asignacion[1] for asignacion in asignaciones]

    # Si el avión tiene tareas de tipo 2 (T2)
    if avion["T2"] > 0:
        # Seleccionamos las franjas que corresponden a tareas de tipo 2
        franjas_t2 = franjas_asignadas[:avion["T2"]]

        # Si el avión también tiene tareas de tipo 1 (T1), comprobamos que todas las T2 sean antes que las T1
        if avion["T1"] > 0:
            franjas_t1 = franjas_asignadas[avion["T2"]:avion["T2"] + avion["T1"]]
            # Verificar que todas las franjas de tipo 2 sean antes que las franjas de tipo 1
            if max(franjas_t2) >= min(franjas_t1):
                return False  # El último de tipo 2 no puede ser después del primero de tipo 1

    return True


def verificar_r5(asignaciones, talleres_std, talleres_spc, prk):
    # nos tenemos en cuenta cada avion de forma individiual, iremos revisando cada posicion
    # con algún avion asignado y verificando que haya al menos un vecino libre
    # Obtener las posiciones asignadas
    posiciones_asignadas = set()

    for asignacion in asignaciones:
        if asignacion is not None:
            posiciones_asignadas.add(asignacion)

    # Dimensiones de la matriz de talleres y parkings
    max_filas = len(talleres_std)
    max_columnas = len(talleres_std[0])  # Suponemos que todas las matrices tienen el mismo tamaño

    # Para cada posición asignada, verificamos las posiciones adyacentes
    for pos in posiciones_asignadas:
        if isinstance(pos, tuple) and len(pos) == 2:  # Verificamos que sea una tupla de (x, y)
            x, y = pos

            # Calculamos las posiciones adyacentes válidas
            adyacentes = [
                (x - 1, y),  # Arriba
                (x + 1, y),  # Abajo
                (x, y - 1),  # Izquierda
                (x, y + 1),  # Derecha
            ]

            # Filtramos las posiciones adyacentes para asegurarnos de que estén dentro del rango
            # Por ejemplo, si estamos en la casilla (0,0) que no busque vecinos en la (-1, 0)
            adyacentes = [
                (ax, ay)
                for ax, ay in adyacentes
                if 0 <= ax < max_filas and 0 <= ay < max_columnas
            ]

            # Si todas las posiciones adyacentes están ocupadas...
            if all(pos_ady in posiciones_asignadas for pos_ady in adyacentes):
                # DEBUG
                # print(f"Restricción rota: Posición {pos} con adyacentes ocupados {adyacentes}")
                return False

    return True


def verificar_r6(asignaciones, talleres_std, talleres_spc, prk, aviones, franja):
    # Filtrar los aviones tipo JMB en la franja específica
    posiciones_jumbo = set()

    # Filtrar los aviones JMB que están asignados a la franja actual y con tareas asignadas
    aviones_jumbo = [avion for avion in aviones if avion['tipo'] == 'JMB' and (avion['T1'] == franja or avion['T2'] == franja)]

    # Recoger las posiciones asignadas de los aviones Jumbo
    for avion, asignacion in zip(aviones_jumbo, asignaciones):
        if asignacion is not None:  # Si el avión tiene asignación
            posiciones_jumbo.add(asignacion)
    # Así sacamos todas las posiciones de los JMB para poder verficiar las adyacentes,
    # y poder quitarlas de nuestras soluciones

    # Dimensiones de los talleres
    max_filas = len(talleres_std)
    max_columnas = len(talleres_std[0])
    # para definir la matriz de los talleres, en la que comprobaremos las adyacencias

    # Verificar si hay aviones Jumbo en talleres adyacentes
    for pos in posiciones_jumbo:
        if isinstance(pos, tuple) and len(pos) == 2:  # Asegurar formato correcto
            x, y = pos

            # Calcular las posiciones adyacentes válidas (sin diagonales x+1,y+1)
            adyacentes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            adyacentes = [
                (ax, ay) for ax, ay in adyacentes
                if 0 <= ax < max_filas and 0 <= ay < max_columnas
            ]

            # Si algún adyacente está ocupado por otro JUMBO en la misma franja, la restriccion no se cumple
            if any(pos_ady in posiciones_jumbo for pos_ady in adyacentes):
                return False

    return True


# ###################################################################################################################


# ----------------------MAIN BUENO-------------

def main():
    # Verifica que se pase el argumento
    if len(sys.argv) < 2:
        print("Uso: python CSPMaintenance.py <ruta_archivo>")
        sys.exit(1)

    # Recoge la ruta del archivo desde sys.argv
    ruta_archivo = sys.argv[1]
    # podemos hacer un simple replace, pues la salida va junto con el fichero de entrada
    ruta_salida = ruta_archivo.replace(".txt", ".csv")

    try:
        with open(ruta_archivo, 'r') as archivo:
            print(f"Leyendo archivo: {ruta_archivo}\n")
            for linea in archivo:
                print(linea.strip())  # Procesa cada línea
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no se encuentra.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    # Sacamos los datos de entrada
    n_franjas_horarias, matriz_size, talleres_std, talleres_spc, prk, aviones = leer_entrada(ruta_archivo)

    # DEBUG: comprobar que funciona el input
    """print(f"Franjas horarias: {n_franjas_horarias}")
    print(f"Tamaño de matriz: {matriz_size}")
    print(f"Talleres estándar: {talleres_std}")
    print(f"Talleres especialistas: {talleres_spc}")
    print(f"Parkings: {prk}")
    print(f"Aviones: {aviones}")"""

    # Modelar problema
    problema = modelar_problema(n_franjas_horarias, matriz_size, talleres_std, talleres_spc, prk, aviones)

    # Calculamos las soluciones con python-constraint
    soluciones = problema.getSolutions()

    # Construimos la lista de posiciones
    posiciones = [("STD", coord) for coord in talleres_std] + \
                 [("SPC", coord) for coord in talleres_spc] + \
                 [("PRK", coord) for coord in prk]

    # Genera el resultado
    generar_resultado(ruta_salida, soluciones, aviones, n_franjas_horarias, posiciones)
    print(f"Soluciones guardadas en {ruta_salida}")


if __name__ == "__main__":
    main()

"""

# ------------------------------------------MAIN---------------------------------

txt = "Franjas: 4"
print(txt.strip(".Franjas: "))

txt2 = "2x3"
# split devuelve una lista
print(list(map(int, txt2.split("x")))) # map aplica "int" a cada elemento de la lista

talleres = "STD:(0,1) (1,0) (1,1) (1,2) (1,3) (2,0) (2,2) (3,3) (4,1) (4,2)\n"
tupla_talleres_str = talleres.strip(".STD:").split(" ")
tupla_talleres = []
for elem in tupla_talleres_str:
    elem_sin_parentesis = elem.strip("()\n")
    x, y = elem_sin_parentesis.split(",")
    tupla_talleres.append((int(x), int(y)))

print(tupla_talleres)
print(tupla_talleres[9])
"""
