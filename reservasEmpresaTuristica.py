#--------------------------------------------------------------------------------------------------------------
#FUNCIONES
#--------------------------------------------------------------------------------------------------------------
def diasEnElMes(_mes): 
#Esta función sirve para saber cuantos dias tienen los meses
    if _mes in(4,6,9,11):
        _dias = 30
    elif _mes == 2:
        _dias = 28
    else:
        _dias = 31 
    return _dias

def pedirEntero(_mensajeInput, _mensajeError):
#Esta función sirve para pedir un valor y validar si es un múmero entero utilizando excepciones si no se ingresa nada o si se ingresa un valor que no se pueda convertir a un entero entonces se debe mostrar el mensaje de error y volver a pedir el valor

    try:
        num = int(input(_mensajeInput))
    except ValueError:
        print(_mensajeError)
        num = pedirEntero(_mensajeInput, _mensajeError)
    return num


def mostrarGuias(_pathGuias):
#Esta función sirve simplemente para mostrar el listado de guías de turismo

    try:
        archivoGuias = open(_pathGuias, mode="r", encoding="utf-8")
        for linea in archivoGuias:
            lista = linea.strip("\n").split("\t")
            print(lista[0] + " " + lista[1])
    except (OSError, FileNotFoundError) as detalle:
        print(f"Error: {detalle}")
    finally:
        try:
            archivoGuias.close()
        except:
            pass

def funcionCodigoGuias(_pathGuias):
#Esta función sirve simplemente para guardar el codigo de los guias en una lista para proximamente realizar validaciones sobre la misma

    listaCodigoGuias = []

    try:
        archivoGuias = open(_pathGuias, mode="r", encoding="utf-8")
        for linea in archivoGuias:
            lista = linea.strip("\n").split("\t")
            listaCodigoGuias.append(lista[0]) #Carga de codigos de los guias
    except (OSError, FileNotFoundError) as detalle:
        print(f"Error: {detalle}")
    finally:
        try:
            archivoGuias.close()
        except:
            pass
    return listaCodigoGuias

def reservarDestino(_pathReservas, _pathGuias, _destinosTuristicos):
#Esta función permite agregar reservas de destinos al archivo de texto (delimitado por tabulación).

    cadenaCaracter = "" #En esta cadena se concatenará el texto a cargar en el archivo
    mensajeInput = ""   #Variable modificable para utilizar como mensaje de entrada cada vez que se tenga que llamar a la función pedirEntero
    mensajeError = ""   #Variable modificable para utilizar como mensaje de error cada vez que se tenga que llamar a la función pedirEntero
    diasOcupados = []   #Lista en donde almacenar los días con reserva asignada tomando los datos desde el archivo y para el mes ingresado 
    
    try:
        mostrarGuias(_pathGuias) #Mostrar el listado de guías de turismo para ayudar a la posterior carga de códigos

        codigosDeLosGuias = funcionCodigoGuias(_pathGuias)
        mensajeInput = "Ingresar el código del guía [100 a 500]: "
        mensajeError = "Error, código inválido vuelva a intentar."

        codigoGuia = pedirEntero(mensajeInput, mensajeError)

        while str(codigoGuia) not in codigosDeLosGuias:
            print("codigo fuera de rango")
            codigoGuia = pedirEntero(mensajeInput, mensajeError)

        mensajeInput = "Ingresar el mes de la reserva: "
        mensajeError = "Error, mes inválido, vuelva a intentar"

        mes = pedirEntero(mensajeInput, mensajeError)

        while mes < 1 or mes > 12:
            print("Mes inexistente")
            mes = pedirEntero(mensajeInput, mensajeError)

        print("DÍAS OCUPADOS -------------")
        archivoReservas = open(_pathReservas, mode="r", encoding="utf-8")
        for linea in archivoReservas:
            lista = linea.strip("\n").split("\t")
            if lista[2] == str(mes):
                diasOcupados.append(int(lista[1]))
        diasOcupados.sort()
        diasOcupados = list(set(diasOcupados))
        print(diasOcupados)

        diasDelMes = diasEnElMes(mes)

        mensajeInput = "Ingresar el día de reserva: "
        mensajeError = "Error, día inválido."

        diaReserva = pedirEntero(mensajeInput, mensajeError)
        while diaReserva > diasDelMes or diaReserva < 1 or (diaReserva <= 31 and diaReserva > diasDelMes) or diaReserva in diasOcupados:
            if diaReserva < 1 or diaReserva > 31:
                print("Día inválido.")
            elif diaReserva > diasDelMes:
                print("Mes con menor cantidad de días.")
            elif diaReserva in diasOcupados:
                print("Día ya reservado.")
            diaReserva = pedirEntero(mensajeInput, mensajeError)

        
        destinoTuristicoDelTurista = input("Ingresar el destino turístico [ALTURAS, RIOS, SALINA, QUEBRADA]: ").upper()

        while destinoTuristicoDelTurista not in _destinosTuristicos:
            print("Error! Destino inválido, vuelva a intentar.")
            destinoTuristicoDelTurista = input("Ingresar el destino turístico [ALTURAS, RIOS, SALINA, QUEBRADA]: ").upper()

        nombreDelTurista = input("Ingresar el nombre del turista: ").upper()

        apellidoDelTurista = input("Ingresar el apellido del turista: ").upper()

        archivoReservas = open(_pathReservas, mode="a", encoding="utf-8")
        cadenaCaracter = "\n" + nombreDelTurista + " " + apellidoDelTurista + "\t" + str(diaReserva) + "\t" + str(mes) + "\t" + destinoTuristicoDelTurista + "\t" + str(codigoGuia)
    except (OSError, FileNotFoundError) as detalle:
        print(f"Error: {detalle}")
    finally:
        try:
            archivoReservas.close()
            archivoReservas = open(_pathReservas, mode="a", encoding="utf-8")

            archivoReservas.write(cadenaCaracter)
            archivoReservas.close()
        except:
            pass

    print("Reserva cargada con exito!")


def mostrarTuristasSegunGuia(_pathReservas, _pathGuias):
#Esta función muestra todos los turistas según un guía turístico ingresado

    listaDeTuritas = [] #En esta lista voy a cargar los turistas que esten con el codigo de guia de turismo que ingrese el usuario

    print("GUÍAS DE TURISMO -------------")
    mostrarGuias(_pathGuias)

    mensajeInput = "Ingresar el código del guía [100 a 500]: "
    mensajeError = "Error, código inválido vuelva a intentar."

    codigoGuia = pedirEntero(mensajeInput, mensajeError)
    codigosDeLosGuias = funcionCodigoGuias(_pathGuias)

    while codigoGuia not in codigosDeLosGuias:
        print("codigo fuera de rango")
        codigoGuia = pedirEntero(mensajeInput, mensajeError)

    print("LISTADO DE TURISTAS -------------")
    try:
        archivoReservas = open(_pathReservas, mode="r", encoding="utf-8")
        for linea in archivoReservas: 
            lista = linea.strip("\n").split("\t")
            for i in range(len(lista)):
                if str(codigoGuia) in lista:
                    listaDeTuritas.append(lista[0])
        listaDeTuritas = list(set(listaDeTuritas))
        for i in range(len(listaDeTuritas)):
            print(listaDeTuritas[i])
    except (OSError, FileNotFoundError) as detalle:
        print(f"Error: {detalle}")
    finally:
        try:
            archivoReservas.close()
        except:
            pass

#--------------------------------------------------------------------------------------------------------------
# Inicialización de variables
#--------------------------------------------------------------------------------------------------------------
pathReservas = "(ruta del archivo con las reservas, dentro de las "")"  #variable string para el path completo del archivo de reservas
pathGuias = "(ruta del archivo con los guias, dentro de las "")"  #variable string para el path completo del archivo de guías 
destinosTuristicos = ["ALTURAS", "RIOS", "SALINA", "QUEBRADA"]

#--------------------------------------------------------------------------------------------------------------
# Bloque de menú
#--------------------------------------------------------------------------------------------------------------
while True:
    while True:
        try:
            print()
            print("-------------------------------------------")
            print("MENÚ DEL SISTEMA")
            print("-------------------------------------------")
            print("[1] Reservar un Destino")
            print("[2] Mostrar Turistas según Guía")
            print("-------------------------------------------")
            print("[0] Salir")
            print("-------------------------------------------")
            print()
            opcion = input("Seleccione una opción: ")
            if opcion in ["0","1","2"]: #Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        except ValueError:
            input("Opción inválida. Presione ENTER para volver a seleccionar.")

    if opcion == "0":
        exit()

    elif opcion == "1":  
       reservarDestino(pathReservas, pathGuias, destinosTuristicos)
        
    elif opcion == "2":   
        mostrarTuristasSegunGuia(pathReservas, pathGuias)
    print()
    input("Presione ENTER para volver al menú.")