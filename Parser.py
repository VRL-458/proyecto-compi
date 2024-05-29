def parser_programa(input):
  print("Soy el parser programa y recibi: ", input)

  c1 = input[0][1] == "HOLA"
  if c1:
     c3 = input[-1][1] == "ADIOS"
     if c3:
        c2 = parser_ordenes(input[1:len(input)-1])
        return c2
  return False


def parser_ordenes(input):
  print("Soy el parser ordenes y recibi: ", input)

  res = False
  if len(input) == 0:
    return True, input

  (res, input) = parser_asignacion_variable(input)
  if not res:
    (res, input) = parser_condicion(input)
    if not res:
      (res, input) = parser_ciclo(input)
      if not res:
        return (False, input)

  return parser_ordenes(input)

def parser_asignacion_variable(input):
  print("Soy el parser asignacion y recibi: ", input)

  res = False
  if input[0][1] == "ASIGNA" and input[1][1] == "identificador" and input[2][1] == "=":
    (res, input) = parser_expresion(input[3:])
    if res:
      if input[0][1] == "PORFA":
        res = True
        input = input[1:]

  return (res, input)

def parser_expresion(input):
  print("Soy el parser expresion y recibi: ", input)

  res = False
  (res, input) = parser_operacion(input)
  if not res:
    (res, input) = parser_valor(input)

  return (res, input)

def parser_valor(input):
  print("Soy el parser valor y recibi: ", input)

  res = False
  if input[0][1] == "cadena" or input[0][1] == "numero" or input[0][1] == "identificador":
    res = True
    input = input[1:]

  return(res, input)

def parser_operacion(input):
  print("Soy el parser operacion y recibi: ", input)
  res = False
  if (input[0][1] == "numero" or input[0][1] == "identificador") and input[1][1] == "operador_aritmetico" and (input[2][1] == "numero" or input[2][1] == "identificador"):
    res = True
    input = input[3:]
  return (res, input)

def parser_condicion(input):
  print("Soy el parser condicion y recibi: ", input)

  res = False
  if input[0][1] == "SI" and input[1][1] == "(":
    (res, input) = parser_comparacion(input[2:])
    if res:
      if input[0][1] == ")" and input[1][1] == "ENTONCES":

        porfa = 1
        sino = 1
        input = input[2:]
        nuevaLista = []
        aux = input.copy()
        for i in input:
          if i[1] == "SI":
            porfa += 1
            sino += 1
          elif i[1] == "MIENTRAS" or i[1] == "ASIGNA":
            porfa += 1
          elif i[1] == "PORFA":
            if porfa == sino:
              sino -= 1
            porfa -= 1
            if porfa == 0:
              break
          elif i[1] == "SINO":
            sino -= 1
            if sino == 0:
              break
          nuevaLista.append(i)
          aux = aux[1:]
        input = aux.copy()


        (res, _) = parser_ordenes(nuevaLista)
        if res:
          if input[0][1] == "PORFA":
            res = True
            input = input[1:]
          elif input[0][1] == "SINO":


            input = input[1:]
            nuevaLista = []
            aux = input.copy()
            _match = 0
            for i in input:
              if i[1] == "ASIGNA" or i[1] == "SI" or i[1] == "MIENTRAS":
                _match += 1
              if i[1] == "PORFA":
                if _match > 0:
                  _match -= 1
                else:
                  break
              nuevaLista.append(i)
              aux = aux[1:]
            input = aux.copy()


            (res, _) = parser_ordenes(nuevaLista)
            if res:
              if input[0][1] == "PORFA":
                res = True
                input = input[1:]

  return (res, input)

def parser_ciclo(input):
  print("Soy el parser ciclo y recibi: ", input)
  res = False
  if input[0][1] == "MIENTRAS" and input[1][1] == "(":
    (res, input) = parser_comparacion(input[2:])
    if res:
      if input[0][1] == ")" and input[1][1] == "HAZ":


        input = input[2:]
        nuevaLista = []
        aux = input.copy()
        _match = 0
        for i in input:
          if i[1] == "ASIGNA" or i[1] == "SI" or i[1] == "MIENTRAS":
            _match += 1
          if i[1] == "PORFA":
            if _match > 0:
              _match -= 1
            else:
              break
          nuevaLista.append(i)
          aux = aux[1:]
        input = aux.copy()


        (res, _) = parser_ordenes(nuevaLista)
        if res:
          if input[0][1] == "PORFA":
            res = True
            input = input[1:]
  return (res, input)


def parser_comparacion(input):
  print("Soy el parser comparacion y recibi: ", input)
  res = False
  if ((input[0][1] == "numero" and input[2][1] == "numero") or (input[0][1] == "cadena" and input[2][1] == "cadena") or input[0][1] == "identificador" or input [2][1] == "identificador")  and input[1][1] == "operador_comparacion":
    res = True
    input = input[3:]
  return (res, input)


input = [('HOLA', 'HOLA'), ('SI', 'SI'), ('(', '('), ('x', 'identificador'), ('==', 'operador_comparacion'), ('1', 'numero'), (')', ')'), ('ENTONCES', 'ENTONCES'), ('ASIGNA', 'ASIGNA'), ('x', 'identificador'), ('=', '='), ('4', 'numero'), ('PORFA', 'PORFA'), ('MIENTRAS', 'MIENTRAS'), ('(', '('), ('x', 'identificador'), ('==', 'operador_comparacion'), ('1', 'numero'), (')', ')'), ('HAZ', 'HAZ'), ('SI', 'SI'), ('(', '('), ('x', 'identificador'), ('==', 'operador_comparacion'), ('0', 'numero'), (')', ')'), ('ENTONCES', 'ENTONCES'), ('ASIGNA', 'ASIGNA'), ('x', 'identificador'), ('=', '='), ('4', 'numero'), ('PORFA', 'PORFA'), ('PORFA', 'PORFA'), ('PORFA', 'PORFA'), ('SI', 'SI'), ('(', '('), ('y', 'identificador'), ('==', 'operador_comparacion'), ('3', 'numero'), (')', ')'), ('ENTONCES', 'ENTONCES'), ('ASIGNA', 'ASIGNA'), ('y', 'identificador'), ('=', '='), ('1', 'numero'), ('PORFA', 'PORFA'), ('SINO', 'SINO'), ('SI', 'SI'), ('(', '('), ('y', 'identificador'), ('==', 'operador_comparacion'), ('0', 'numero'), (')', ')'), ('ENTONCES', 'ENTONCES'), ('ASIGNA', 'ASIGNA'), ('dani', 'identificador'), ('=', '='), ('0', 'numero'), ('PORFA', 'PORFA'), ('PORFA', 'PORFA'), ('PORFA', 'PORFA'), ('PORFA', 'PORFA'), ('ADIOS', 'ADIOS') ]
print(parser_programa(input))