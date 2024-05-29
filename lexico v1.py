import re

# Palabras reservadas
palabras_reservadas = [
    'HOLA', 'ADIOS', 'SINO', 'SI', 'ENTONCES', 'PORFA', 'MIENTRAS', 'HAZ', 'LEE', 'ESCRIBE', '(', ')', 'ASIGNA', '='
]

# Operadores aritméticos
operadores_aritmeticos = ['+', '-', '*', '/']

# Operadores de comparación
operadores_comparacion = ['==', '>', '<', '>=', '<=', '!=', 'YY', 'OO']

# Tokens identificadores
TOKEN_OPERADOR_ARITMETICO = 'operador_aritmetico'
TOKEN_OPERADOR_COMPARACION = 'operador_comparacion'
TOKEN_IDENTIFICADOR = 'identificador'
TOKEN_NUMERO = 'numero'
TOKEN_CADENA = 'cadena'
TOKEN_BOOLEANO = 'booleano'
TOKEN_ASIGNACION = 'asignacion'
TOKEN_PARENTESIS_IZQUIERDO = 'parentesis_izquierdo'
TOKEN_PARENTESIS_DERECHO = 'parentesis_derecho'
TOKEN_FIN_LINEA = 'fin_linea'

def verificar_palabra_reservada(codigo, posicion):
    for palabra in palabras_reservadas:
        longitud = len(palabra)
        if posicion + longitud <= len(codigo) and codigo[posicion:posicion + longitud] == palabra:
            if palabra == '=' and (posicion + 1 < len(codigo) and codigo[posicion + 1] == '='):
                continue  # Evitar tratar '==' como palabra reservada '='
            return (palabra, palabra)
    return None

def verificar_operador_aritmetico(codigo, posicion):
    for operador in operadores_aritmeticos:
        if posicion < len(codigo) and codigo[posicion] == operador:
            return (TOKEN_OPERADOR_ARITMETICO, operador)
    return None

def verificar_operador_comparacion(codigo, posicion):
    for operador in operadores_comparacion:
        longitud = len(operador)
        if posicion + longitud <= len(codigo) and codigo[posicion:posicion + longitud] == operador:
            return (TOKEN_OPERADOR_COMPARACION, operador)
    return None

def verificar_identificador(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion].isalpha():
        identificador = codigo[posicion]
        posicion += 1
        while posicion < len(codigo) and codigo[posicion].isalpha():
            identificador += codigo[posicion]
            posicion += 1
        return (TOKEN_IDENTIFICADOR, identificador)
    return None

def verificar_numero(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion].isdigit():
        numero = codigo[posicion]
        posicion += 1
        while posicion < len(codigo) and codigo[posicion].isdigit():
            numero += codigo[posicion]
            posicion += 1
        if posicion < len(codigo) and codigo[posicion] == '.':
            numero += codigo[posicion]
            posicion += 1
            while posicion < len(codigo) and codigo[posicion].isdigit():
                numero += codigo[posicion]
                posicion += 1
        return (TOKEN_NUMERO, numero)
    return None

def verificar_cadena(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion] == '"':
        posicion += 1
        cadena = ""
        while posicion < len(codigo) and codigo[posicion] != '"':
            cadena += codigo[posicion]
            posicion += 1
        if posicion < len(codigo) and codigo[posicion] == '"':
            posicion += 1
            return (TOKEN_CADENA, cadena), posicion
    return None, posicion

def analizar_lexico(codigo):
    tokens_encontrados = []
    posicion = 0

    while posicion < len(codigo):
        token = None

        if codigo[posicion].isspace():
            posicion += 1
            continue
        if codigo[posicion] == '\\':
            posicion += 2
            continue

        token = verificar_palabra_reservada(codigo, posicion)
        if token is None:
            token = verificar_operador_comparacion(codigo, posicion)
        if token is None:
            token = verificar_operador_aritmetico(codigo, posicion)
        if token is None:
            token, posicion = verificar_cadena(codigo, posicion)
        if token is None:
            token = verificar_identificador(codigo, posicion)
        if token is None:
            token = verificar_numero(codigo, posicion)

        if token is not None:
            tokens_encontrados.append(token)
            if isinstance(token, tuple) and isinstance(token[1], str):
                posicion += len(token[1])
        else:
            print(f"Error léxico: Caracter no reconocido '{codigo[posicion]}' en la posición {posicion}")
            posicion += 1

    return tokens_encontrados

def convertir_codigo():
    comentario_bloque = False
    comentario_linea = False
    count = 0
    resultado = ""

    with open('textocodigo.txt', 'r') as archivo:
        contenido = archivo.read().replace(' ', '')  # Eliminar espacios en blanco

        while count < len(contenido):
            if comentario_bloque:
                if contenido[count:count + 2] == "*/":
                    comentario_bloque = False
                    count += 2
                else:
                    count += 1
            elif comentario_linea:
                if contenido[count] == "\n":
                    resultado += "\\n"
                    comentario_linea = False
                count += 1
            else:
                if contenido[count:count + 2] == "/*":
                    comentario_bloque = True
                    count += 2
                elif contenido[count:count + 2] == "//":
                    comentario_linea = True
                    count += 2
                else:
                    if contenido[count] == "\n":
                        resultado += "\\n"
                    elif contenido[count] == "\t":
                        resultado += "\\t"
                    else:
                        resultado += contenido[count]
                    count += 1

    return resultado


# Obtener el contenido del archivo
contenido = convertir_codigo()
print("Codigo: \n", contenido)
# Realizar el análisis léxico
tokens_encontrados = analizar_lexico(contenido)

# Imprimir los tokens encontrados
print('[', end='')
for token in tokens_encontrados:
    print(f'(\'{token[1]}\', \'{token[0]}\'), ', end='')
print(']')import re

# Palabras reservadas
palabras_reservadas = [
    'HOLA', 'ADIOS', 'SINO', 'SI', 'ENTONCES', 'PORFA', 'MIENTRAS', 'HAZ', 'LEE', 'ESCRIBE', '(', ')', 'ASIGNA', '='
]

# Operadores aritméticos
operadores_aritmeticos = ['+', '-', '*', '/']

# Operadores de comparación
operadores_comparacion = ['==', '>', '<', '>=', '<=', '!=', 'YY', 'OO']

# Tokens identificadores
TOKEN_OPERADOR_ARITMETICO = 'operador_aritmetico'
TOKEN_OPERADOR_COMPARACION = 'operador_comparacion'
TOKEN_IDENTIFICADOR = 'identificador'
TOKEN_NUMERO = 'numero'
TOKEN_CADENA = 'cadena'
TOKEN_BOOLEANO = 'booleano'
TOKEN_ASIGNACION = 'asignacion'
TOKEN_PARENTESIS_IZQUIERDO = 'parentesis_izquierdo'
TOKEN_PARENTESIS_DERECHO = 'parentesis_derecho'
TOKEN_FIN_LINEA = 'fin_linea'

def verificar_palabra_reservada(codigo, posicion):
    for palabra in palabras_reservadas:
        longitud = len(palabra)
        if posicion + longitud <= len(codigo) and codigo[posicion:posicion + longitud] == palabra:
            if palabra == '=' and (posicion + 1 < len(codigo) and codigo[posicion + 1] == '='):
                continue  # Evitar tratar '==' como palabra reservada '='
            return (palabra, palabra)
    return None

def verificar_operador_aritmetico(codigo, posicion):
    for operador in operadores_aritmeticos:
        if posicion < len(codigo) and codigo[posicion] == operador:
            return (TOKEN_OPERADOR_ARITMETICO, operador)
    return None

def verificar_operador_comparacion(codigo, posicion):
    for operador in operadores_comparacion:
        longitud = len(operador)
        if posicion + longitud <= len(codigo) and codigo[posicion:posicion + longitud] == operador:
            return (TOKEN_OPERADOR_COMPARACION, operador)
    return None

def verificar_identificador(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion].isalpha():
        identificador = codigo[posicion]
        posicion += 1
        while posicion < len(codigo) and codigo[posicion].isalpha():
            identificador += codigo[posicion]
            posicion += 1
        return (TOKEN_IDENTIFICADOR, identificador)
    return None

def verificar_numero(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion].isdigit():
        numero = codigo[posicion]
        posicion += 1
        while posicion < len(codigo) and codigo[posicion].isdigit():
            numero += codigo[posicion]
            posicion += 1
        if posicion < len(codigo) and codigo[posicion] == '.':
            numero += codigo[posicion]
            posicion += 1
            while posicion < len(codigo) and codigo[posicion].isdigit():
                numero += codigo[posicion]
                posicion += 1
        return (TOKEN_NUMERO, numero)
    return None

def verificar_cadena(codigo, posicion):
    if posicion < len(codigo) and codigo[posicion] == '"':
        posicion += 1
        cadena = ""
        while posicion < len(codigo) and codigo[posicion] != '"':
            cadena += codigo[posicion]
            posicion += 1
        if posicion < len(codigo) and codigo[posicion] == '"':
            posicion += 1
            return (TOKEN_CADENA, cadena), posicion
    return None, posicion

def analizar_lexico(codigo):
    tokens_encontrados = []
    posicion = 0

    while posicion < len(codigo):
        token = None

        if codigo[posicion].isspace():
            posicion += 1
            continue
        if codigo[posicion] == '\\':
            posicion += 2
            continue

        token = verificar_palabra_reservada(codigo, posicion)
        if token is None:
            token = verificar_operador_comparacion(codigo, posicion)
        if token is None:
            token = verificar_operador_aritmetico(codigo, posicion)
        if token is None:
            token, posicion = verificar_cadena(codigo, posicion)
        if token is None:
            token = verificar_identificador(codigo, posicion)
        if token is None:
            token = verificar_numero(codigo, posicion)

        if token is not None:
            tokens_encontrados.append(token)
            if isinstance(token, tuple) and isinstance(token[1], str):
                posicion += len(token[1])
        else:
            print(f"Error léxico: Caracter no reconocido '{codigo[posicion]}' en la posición {posicion}")
            posicion += 1

    return tokens_encontrados

def convertir_codigo():
    comentario_bloque = False
    comentario_linea = False
    count = 0
    resultado = ""

    with open('textocodigo.txt', 'r') as archivo:
        contenido = archivo.read().replace(' ', '')  # Eliminar espacios en blanco

        while count < len(contenido):
            if comentario_bloque:
                if contenido[count:count + 2] == "*/":
                    comentario_bloque = False
                    count += 2
                else:
                    count += 1
            elif comentario_linea:
                if contenido[count] == "\n":
                    resultado += "\\n"
                    comentario_linea = False
                count += 1
            else:
                if contenido[count:count + 2] == "/*":
                    comentario_bloque = True
                    count += 2
                elif contenido[count:count + 2] == "//":
                    comentario_linea = True
                    count += 2
                else:
                    if contenido[count] == "\n":
                        resultado += "\\n"
                    elif contenido[count] == "\t":
                        resultado += "\\t"
                    else:
                        resultado += contenido[count]
                    count += 1

    return resultado


# Obtener el contenido del archivo
contenido = convertir_codigo()
print("Codigo: \n", contenido)
# Realizar el análisis léxico
tokens_encontrados = analizar_lexico(contenido)

# Imprimir los tokens encontrados
print('[', end='')
for token in tokens_encontrados:
    print(f'(\'{token[1]}\', \'{token[0]}\'), ', end='')
print(']')