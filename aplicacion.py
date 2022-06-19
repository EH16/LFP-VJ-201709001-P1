# Analizador Lexico
from asyncore import write
import encodings
from logging import exception
import os
import codecs
from pipes import Template
import webbrowser
# Variables

GeneraReporte = False

digitos = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
letras = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A",
          "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
ignorar = " \n\t"
Reporte_tokens = list()
Reporte_AFDs = list()
Reporte_errores = list()
aux_tokens = []


class tokens_reconocidos:
    linea = 0
    columna = 0
    lexema = ""
    token = ""
    patron = ""

class AFDs:
    estado = ""
    caracter = ""
    lexemaR = ""
    siguiente_estado = ""
    token = ""

    

class error:
    linea = 0
    columna = 0  
    lexema = ""  

# Tokens


tokens = {
    "tk_comentario_simple": "//",
    "tk_comentario_dobleA": "/*",
    "tk_comentario_dobleB": "*/",
    "tk_suma": "+",
    "tk_resta": "-",
    "tk_multiplicacion": "*",
    "tk_division": "/",
    "tk_resto": "-",
    "tk_igualacion": "==",
    "tk_diferenciacion": "!=",
    "tk_asignacion": "=",
    "tk_mayor_igual": ">=",
    "tk_mayor": ">",
    "tk_menor_igual": "<=",
    "tk_menor": "<",
    "tk_operador_and": "&&",
    "tk_operdaor_or": "||",
    "tk_operdaor_not": "!",
    "tk_llaveA": "{",
    "tk_llaveB": "}",
    "tk_corcheteA": "[",
    "tk_corcheteB": "]",
    "tk_parentesisA": "(",
    "tk_parentesisB": ")",
    "tk_punto_coma": ";",
    "tk_tipo_int": "int",
    "tk_dato_int": "[0-9]+",
    "tk_tipo_double": "double",
    "tk_tipo_string": "string",
    "tk_tipo_char": "char",
    "tk_dato_string": "[a-zA-Z|0-9|\s][a-zA-Z|0-9|\s]*\"",
    "tk_dato_double": "[0-9]+.[0-9]{1,2}",
    "tk_dato_char": "'[a-zA-Z0-9]'",
    "tk_tipo_boolean": "boolean",
    "tk_dato_boolean": "(true|false)",
    "tk_identificador": "[a-zA-Z_][a-zA-Z0-9_]*",
    "tk_condicional_else": "else",
    "tk_condicional_if": "if",
    "tk_ciclo_while": "while",
    "tk_ciclo_do": "do",
    "tk_reservada_return": "return"


}


def AFDDigito(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    
    listaAux = list()
    for char in lexema:
        if char == " " or char == "\n" or char == "\t":
            break
        if char == ".":
            #print("si retacho")
            return 0
    for char in lexema:
        # print(char)
        if estado == 1:
            if char not in digitos:
                estado = -1
            else:
                afd = AFDs()
                afd.estado = "S1"
                afd.caracter = char
                afd.lexemaR = lexema[0:indiceNuevo]
                afd.siguiente_estado = "S1"
                listaAux.append(afd)

                indiceNuevo = indiceNuevo + 1
        
        if estado == 0:
            # print(type(int(char)))
            if char in digitos:
                estado = 1
                afd = AFDs()
                afd.estado = "S0"
                afd.caracter = char
                afd.lexemaR = " "
                afd.siguiente_estado = "S1"

                listaAux.append(afd)
                indiceNuevo = indiceNuevo + 1
                reconocio = True
            else:
                estado = -1
                reconocio = False
        

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_dato_int":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                #--> GRABA LOS DATOS PARA EL REPORTE DE TOKENS ACEPTADOS
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)
                #<--
                #--> GRABA PARA EL REPORTE DE AFDS
                    afd = AFDs()
                    afd.estado = "S1"
                    afd.caracter = "#"
                    afd.lexemaR = lexema[0:indiceNuevo]
                    afd.siguiente_estado = "S1(Aceptacion)"

                    listaAux.append(afd)
                    aux_tokens.append(token)
                    aux_tokens.append(lexema[0:indiceNuevo])
                    Reporte_AFDs.append(listaAux)
                #<--
            return indiceNuevo

    if estado == 1:
        return True


def AFDDouble(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    decimales = 0
    aux = 0
    for char in lexema:
        aux += 1
        #print (aux)
        if estado == 0:
            if char in digitos:
                estado = 1
                reconocio = True
            else:
                reconocio = False
                estado = -1
        if estado == 2:
            #print("llego a estado 2" + char)
            if char not in digitos or decimales > 2:
                estado = -1
                #print ("error"+char)
            else:
                decimales = decimales + 1
                indiceNuevo = indiceNuevo + 1
        if estado == 1:
            if char not in digitos:
                if char == ".":
                    indiceNuevo = indiceNuevo + 1
                    estado = 2
                    #print("aqui va: "+ char)
                else:
                    #print ("salio un clavo: "+char)
                    reconocio = False
            else:
                indiceNuevo = indiceNuevo + 1

        #print("Este es el estado "+ str(estado))
        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_dato_double":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)      
            return indiceNuevo


def AFDString(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    aux = 0
    for char in lexema:
        aux = aux + 1
        if char == "\"" and aux > 1:
            break
        else:
            if char == "\n":
                print("cadena no completada")
                return 0

    for char in lexema:
        if estado == 1:
            #print ("|"+char)
            if char in letras or char in digitos or char == " ":
                indiceNuevo = indiceNuevo + 1
                # print(indiceNuevo)
            else:
                if char == "\"":
                    estado = -1
                    indiceNuevo = indiceNuevo + 1
                    # print(codigo[indiceNuevo])
                    reconocio = True
                else:
                    return 0
        if estado == 0:
            if char == "\"":
                indiceNuevo = indiceNuevo + 1
                estado = 1
                #print("si paso por estado 0")

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_dato_string":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo


def AFDchar(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    aux = 0
    no_caracteres = 0
    for char in lexema:
        aux = aux + 1
        if char == "\'" and aux > 0:
            break
        else:
            if char == "\n":
                print("char no completo")
                return 0

    for char in lexema:
        if estado == 1:
            #print ("|"+char)
            if ((char in letras or char in digitos or char == " ")
               and (no_caracteres <= 1)):

                indiceNuevo = indiceNuevo + 1
                no_caracteres = no_caracteres + 1
                #print("llego: "+str(indiceNuevo))
            else:
                if char == "\'":
                    estado = -1
                    indiceNuevo = indiceNuevo + 1
                    reconocio = True
                else:
                    # 3
                    #print("char no completo osi")
                    return 0
        if estado == 0:
            if char == "\'":
                indiceNuevo = indiceNuevo + 1
                estado = 1
        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_dato_char":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo


def AFDBoolean(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    no_caracteres = 0
    str_apoyo = ""
    for char in lexema:
        str_apoyo = char
        if estado == 7:
            #print("3no reconoce siguiente: " + char)
            if str_apoyo.casefold() == "e":
                estado = -1
                indiceNuevo = indiceNuevo + 1
                reconocio = True
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 6:
            #print("3no reconoce siguiente: " + char)
            if str_apoyo.casefold() == "s":
                estado = 7
                indiceNuevo = indiceNuevo + 1
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 5:
            #print("3no reconoce siguiente: " + char)
            if str_apoyo.casefold() == "l":
                estado = 6
                indiceNuevo = indiceNuevo + 1
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 4:
            #print("3no reconoce siguiente: " + char)
            if str_apoyo.casefold() == "a":
                estado = 5
                indiceNuevo = indiceNuevo + 1
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 3:
            #print("3no reconoce siguiente: " + char)
            if str_apoyo.casefold() == "e":
                estado = -1
                indiceNuevo = indiceNuevo + 1
                reconocio = True
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 2:
            #print("2no reconoce siguiente: " + str_apoyo.casefold())
            if str_apoyo.casefold() == "u":
                estado = 3
                indiceNuevo = indiceNuevo + 1
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 1:
            #print("1no reconoce siguiente: " + str_apoyo.casefold())
            if str_apoyo.casefold() == "r":
                estado = 2
                indiceNuevo = indiceNuevo + 1
            else:
                #print("boolean no completo osi")
                return 0
        if estado == 0:
            #print("no reconoce siguiente: " + str_apoyo.casefold())

            if str_apoyo.casefold() == "t":
                indiceNuevo = indiceNuevo + 1
                estado = 1
                #print("si paso por estado 0")
            else:
                if str_apoyo.casefold() == "f":
                    indiceNuevo = indiceNuevo + 1
                    estado = 4

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):

            for token, patron in tokens.items():
                if token == "tk_dato_boolean":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo


def AFDIndentificador(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False

    for char in lexema:
        if estado == 1:
            #print ("|"+char)
            if char in letras or char in digitos or char == "_":
                indiceNuevo = indiceNuevo + 1
                # print(indiceNuevo)
            else:
                estado = -1
        if estado == 0:
            if char in letras or char == "_":
                indiceNuevo = indiceNuevo + 1
                reconocio = True
                estado = 1
                #print("si paso por estado 0")

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_identificador":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo


def AFDComentario(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False

    for char in lexema:
        if estado == 2:
            #print ("|"+char)
            if char != "\n":
                indiceNuevo = indiceNuevo + 1
            else:
                if char == "\n":
                    #indiceNuevo = indiceNuevo + 1
                    estado = -1
                # print(indiceNuevo)

        if estado == 1:
            #print ("|"+char)
            if char == "/":
                indiceNuevo = indiceNuevo + 1
                estado = 2
                reconocio = True
                # print(indiceNuevo)
            else:
                return 0
        if estado == 0:
            if char == "/":
                indiceNuevo = indiceNuevo + 1
                estado = 1
                #print("si paso por estado 0")
            else:
                return 0

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            for token, patron in tokens.items():
                if token == "tk_comentario_simple":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+lexema[0:indiceNuevo]+"|token: "
                    #      + token+"|patron: " + patron+"|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = lexema[0:indiceNuevo]
                    nuevo_reconocido.token = token
                    nuevo_reconocido.patron = patron
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo


def AFDComentarioDoble(codigo, indice, linea, columna):
    estado = 0
    # print(str(indice))
    lexema = codigo[indice: len(codigo)]
    indiceNuevo = 0
    reconocio = False
    aux = 0
    cadena = ""

    for char in lexema:
        aux = aux + 1
        if estado == 2:
            #print ("|"+char)
            if char == "*" and lexema[aux] == "/":

                reconocio = True
                estado = -1
                cadena += lexema[aux-1:2]
                indiceNuevo = indiceNuevo + 2
            else:
                if aux + indice == len(codigo):
                    estado = -1
                    reconocio = True
                else:
                    cadena += char
                    indiceNuevo = indiceNuevo + 1

        if estado == 1:
            #print ("|"+char)
            if char == "*":
                cadena += char
                indiceNuevo = indiceNuevo + 1
                estado = 2
                reconocio = True
                # print(indiceNuevo)
            else:
                return 0
        if estado == 0:
            if char == "/":
                cadena += char
                indiceNuevo = indiceNuevo + 1
                estado = 1
                #print("si paso por estado 0")
            else:
                return 0

        if (estado == -1 and reconocio) or (indiceNuevo == len(lexema)):
            cadena = cadena.replace("\n", " ")
            for token, patron in tokens.items():

                if token == "tk_comentario_dobleA":
                    #print("|Linea: "+str(linea)+"|Columna: " + str(columna)+"|Lexema: "+cadena+"|token: "
                    #      + "|Comentario Doble |"+"patron: /* */|")
                    nuevo_reconocido = tokens_reconocidos()
                    nuevo_reconocido.linea = linea
                    nuevo_reconocido.columna = columna
                    nuevo_reconocido.lexema = cadena
                    nuevo_reconocido.token = "tk_comentario_doble"
                    nuevo_reconocido.patron = "/* */"
                    Reporte_tokens.append(nuevo_reconocido)       
            return indiceNuevo

# Cuando se lee un archivo se le envia todo el codigo encontrado en el
# archivo de entrada


def Analizador(codigo):
    reconoce_ignorados = False
    columna = 0
    linea = 1
    indice = 0
    apoyo = 0
    Reporte_AFDs.clear()
    Reporte_errores.clear()
    Reporte_tokens.clear()
    print(len(codigo))
    while indice < len(codigo):
        caracter_actual = codigo[indice]
        EntraFor = False
        reconocido = False

        if caracter_actual == "\n":
            linea += 1
            columna = -1

        columna += 1
        # print(str(columna))
        # Ignora los espacios en blanco, tabulaciones y saltos de linea
        # print("|"+caracter_actual+"|")
        if caracter_actual == " " or caracter_actual == "\n" or caracter_actual == "\t":
            #if caracter_actual == " ":
             #   print("Caracter Ignorado: Espacio")
            #if caracter_actual == "\n":
             #   print("Caracter Ignorado: \\n")
            #if caracter_actual == "\t":
             #   print("Caracter Ignorado: \\t")

            indice += 1
            EntraFor = False
            reconoce_ignorados = True
        else:
            EntraFor = True

        reconocidoAnterior = False
        if EntraFor:
            #print ("Entra con este caracter al for: " + caracter_actual)
            for token, patron in tokens.items():
                if str(caracter_actual).casefold() == patron[0] and caracter_actual != "":
                    #print ("si valida")
                    # print(str(indice)+"|"+str(len(patron)))
                    cadena = codigo[indice: indice + len(patron)]
                    # print("|"+cadena)
                    if (str(cadena).casefold() == patron):
                        if patron == "//" or patron == "/*":
                            break
                        else:
                            # print("|Linea: "+str(linea)+"|Columna: "+ str(columna)+"|Lexema: "+cadena+"|token: "
                            # +token+"|patron: "+ patron+"|")
                            indice = indice + len(cadena)
                            columna = columna + (len(cadena) - 1)
                            # Guarda los reportes
                            nuevo_reconocido = tokens_reconocidos()
                            nuevo_reconocido.linea = linea
                            nuevo_reconocido.columna = columna
                            nuevo_reconocido.lexema = cadena
                            nuevo_reconocido.token = token
                            nuevo_reconocido.patron = patron
                            Reporte_tokens.append(nuevo_reconocido)
                            reconocidoAnterior = True
                            # print(indice)
                            break
                    # else:
                        # print ("No reconocio al evaluar " + cadena
                        #    + " con el patron " + patron)
        if not reconocidoAnterior:
            if caracter_actual in digitos:
                # print("entro")
                dato = AFDDigito(codigo, indice, linea, columna)
                if dato != 0:
                    indice = indice + (dato-1)
                    columna = columna + (dato-1)
                    reconocido = True
                if dato == 0:
                    dato2 = AFDDouble(codigo, indice, linea, columna)
                    indice = indice + (dato2-1)
                    columna = columna + (dato2-1)
                    reconocido = True
            if caracter_actual == "\"":
                #print ("entro")
                dato3 = AFDString(codigo, indice, linea, columna)
                if dato3 != 0:
                    indice = indice + (dato3-1)
                    columna = columna + (dato3-1)
                    reconocido = True
            if caracter_actual == '\'':
                dato4 = AFDchar(codigo, indice, linea, columna)
                if dato4 != 0:
                    indice = indice + (dato4-1)
                    columna = columna + (dato4-1)
                    reconocido = True
            if (caracter_actual in letras or
                    caracter_actual == "_"):
                dato5 = AFDIndentificador(codigo, indice, linea, columna)
                if dato5 != 0:
                    indice = indice + (dato5-1)
                    columna = columna + (dato5-1)
                    reconocido = True
            if (str(caracter_actual).casefold() == "t" or
               str(caracter_actual).casefold() == "f"):
                dato6 = AFDBoolean(codigo, indice, linea, columna)
                if dato6 != 0:
                    indice = indice + (dato6-1)
                    columna = columna + (dato6-1)
                    reconocido = True
            if (caracter_actual == "/" and codigo[indice + 1] == "/"):
                dato7 = AFDComentario(codigo, indice, linea, columna)
                if dato7 != 0:
                    indice = indice + (dato7-1)
                    columna = columna + (dato7-1)
                    reconocido = True
            if (caracter_actual == "/" and codigo[indice + 1] == "*"):

                dato8 = AFDComentarioDoble(codigo, indice, linea, columna)
                if dato8 != 0:
                    indice = indice + (dato8-1)
                    columna = columna + (dato8-1)
                    reconocido = True

            if (caracter_actual != " " and caracter_actual != "\n" and caracter_actual != "\t"):
                indice += 1

            if not reconocido and (caracter_actual != " " and caracter_actual != "\n" and caracter_actual != "\t"):
                #print("|No reconocio " + caracter_actual + " |linea :"
                #      + str(linea) + " |columna: "+str(columna))
                nuevo_error = error()
                nuevo_error.linea = linea
                nuevo_error.columna = columna
                nuevo_error.lexema = caracter_actual
                Reporte_errores.append(nuevo_error)     

            #print("caracter que reviso "+caracter_actual )

    # Si llega hasta aqui, analizo bien el archivo
    globals()['GeneraReporte'] = True


def generaHtml(nombre):
    try:
        mensaje = """
    <html>
        <HEAD><TITLE>"""+nombre+"""</TITLE></HEAD>
        <CENTER><h1><font color=red>"""+nombre+"""</font></h1></CENTER>
        <hr>
        <body>
            <font size=5><h1><center>Reportes</center></h1></font>
        <table width="80%" border="1" style="margin: 0 auto; cellspacing="100">
            <center>
		    <caption>Reporte de tokens Reconocidos</caption> 
            <tr>
                <th>Linea</th>
                <th>Columna</th>
                <th>Lexema</th>
                <th>Token</th>
                <th>Patron</th>
            </tr>"""
        for a in Reporte_tokens:
            mensaje += """
                <tr>
                    <td>"""+str(a.linea)+"""</td>
                    <td>"""+str(a.columna)+"""</td>
                    <td>"""+a.lexema+"""</td>
                    <td>"""+a.token+"""</td>
                    <td>"""+a.patron+"""</td>
                </tr>"""

        mensaje += """
        </center></table><br><br>"""
        aux = 0
        for b in Reporte_AFDs:
            
            mensaje += """<table width="80%" border="1" style="margin: 0 auto; cellspacing="100">
            <center>
		    <caption>Lexema:"""" Token: "+aux_tokens[int(aux)]+"""</caption> 
            <tr>
                <th>Estado</th>
                <th>Caracter</th>
                <th>Lexema Reconocido</th>
                <th>Siguiente Estado</th>
            </tr>"""
            for c in b:
                mensaje += """
                    <tr>
                        <td>"""+c.estado+"""</td>
                        <td>"""+c.caracter+"""</td>
                        <td>"""+c.lexemaR+"""</td>
                        <td>"""+c.siguiente_estado+"""</td>
                    </tr>"""
            mensaje += """</center></table><br>"""
            aux = aux + 1
        mensaje += """
        <hr>
        <br><br>
        <table width="80%" border="1" style="margin: 0 auto; cellspacing="100">
            <center>
		    <caption>Reporte de caracteres no reconocidos</caption> 
            <tr>
                <th>Linea</th>
                <th>Columna</th>
                <th>Lexema</th>
            <tr>"""
        for c in Reporte_errores:
            mensaje += """
                <tr>
                    <td>"""+str(c.linea)+"""</td>
                    <td>"""+str(c.columna)+"""</td>
                    <td>"""+c.lexema+"""</td>
                </tr>"""
        mensaje +="""    
        </body>
    </html>"""

        f = open(nombre, 'w')
        f.writelines(mensaje)
        f.close()
        webbrowser.open_new_tab(nombre)

    except Exception as e:
        raise


def Menu():
    salir = False

    while not salir:
        print("-------------ANALIZADOR LEXICO----------|")
        print("---------------Bienvenido----------------")
        print("|Seleccione una opcion                  |")
        print('''|1. Ingresar ruta del archivo a examinar|
|2. Ingresar nombre del reporte         |
|3. Salir del programa                  |
''')
        opcion = int(input())
        if opcion == 1:
            print("Ingrese la ruta completa del archivo")
            ruta = input(">>")
            try:
                archivo = open(ruta, encoding="utf8").read()
                Analizador(archivo)
            except:
                print ()
                print ("Error: Archivo no encontrado")
                print ()

        if opcion == 2:
            if globals()['GeneraReporte'] == True:
                print("Ingrese el nombre del reporte")
                nombreReporte = input("<<")
                nombreReporte += ".html"
                generaHtml(nombreReporte)
                
                print("Se genero el reporte")
            else:
                print("Debe analizar un archivo primero :D")
                input(">>")
        if opcion == 3:
            print("Saliendo del programa.... ")
            salir = True
        if opcion >= 4:
            print("!Aviso¡:   Opcion Invalida")
            print


Menu()
