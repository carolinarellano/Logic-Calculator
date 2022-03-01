def divideProposition(proposition):
    syntaxStatus = checkSyntax(proposition)
    if syntaxStatus == 'Valid':
        dividedProposition = []
        getPrimitives(proposition, dividedProposition)
        negatePrimitives(proposition, dividedProposition)
        getOperations(proposition, dividedProposition)
        dividedProposition = sorted(dividedProposition, key=len)
        return dividedProposition
    else:
        return syntaxStatus

def checkSyntax(proposition):
    errorList = {
        '0': 'Valid',
        '00': 'Existen paréntesis\nsin abrir o cerrar',
        '01': 'No hay primitivas en\nla proposicion',
        '02': 'Existen proposiciones\nno separadas por un\noperador o dos operadores juntos',
        '03': 'La proposición\nestá incompleta'
    }

    primitives = ['p', 'q', 'r', 't', 'c']
    operators = ['∧', '∨', '→', '⟷']

    # Error 00: Parentesis sin abrir o cerrar

    if proposition.count('(') != proposition.count(')'):
        return errorList['00']

    # Error 01: Proposicion sin primitivas

    errorFlag = 0  # Si llega a 5, no existen primitivas en la proposicion
    for primitive in primitives:
        if primitive not in proposition:
            errorFlag += 1
    if errorFlag == 5:
        return errorList['01']

    # Error 02: 2 operadores o 2 proposiciones primitivas juntas

    for i, char in enumerate(proposition):
        if char in primitives:
            if i != 0:
                if proposition[i - 1] in primitives:
                    return errorList['02']
            if i != len(proposition) - 1:
                if proposition[i + 1] == '~' and i != len(proposition) - 1:
                    return errorList['02']
        if char in operators and proposition[i - 1] in operators:
            return errorList['02']

        # Error 03: Operaciones con falta de operandos

        if proposition[i - 2:i] == '()' or proposition[i + 1:i + 3] == '()':
            return errorList['03']
    if proposition[-1] in operators or proposition[0] in operators:
        return errorList['03']

    return errorList['0']




def getPrimitives(proposition, columns):
    primitives = ['p', 'q', 'r', 't', 'c']

    for primitive in primitives:
        if primitive in proposition:
            columns.append(primitive)



def negatePrimitives(proposition, columns):
    for i, char in enumerate(proposition):
        if char == '~':
            negative = f'~{proposition[i + 1]}'
            columns.append(negative)




def getOperations(proposition, columns):
    operators = ['∧', '∨', '→', '⟷']

    # Quitar paréntesis innecesarios

    if proposition[0] == '(' and proposition[-1] == ')':
        if proposition.find(')') == -1:
            proposition = proposition[1:-1]

    # En caso de doble parentesis para la misma expresion, se eliminan

    for i, char in enumerate(proposition):
        if char == '(' and proposition[i + 1] == '(':
            closingParenthesis = proposition.find(')', i)
            if proposition[closingParenthesis + 1] == ')':
                proposition = proposition[:i] + proposition[i + 1:]
                proposition = proposition[:closingParenthesis] + proposition[closingParenthesis + 1:]

    # Dividir por operador

    for i, char in enumerate(proposition):
        if char in operators:
            if char != '→' and char != '⟷':
                if proposition[i - 1] != ')' and proposition[i + 1] != '(':
                    start = i - 1
                    end = i + 2
                    if proposition[i + 1] == '~':
                        end = i + 3
                    if proposition[i - 2] == '~':
                        start = i - 2
                    operation = proposition[start:end]
                    appendColumns(operation, columns)
            else:
                start = i - 1
                if proposition[i - 2] == '~':
                    start = i - 2
                if proposition[i - 1] == ')':
                    start = proposition[i::-1].find('(')
                    start = i - start

                if proposition[i + 1] == '(':
                    end = proposition.find(')', i) - 1
                else:
                    end = len(proposition)
                if proposition[i + 1] == '~':
                    end = i + 2
                if proposition[i + 1] == '(':
                    end = proposition.find(')', i)
                operation = proposition[start:end + 1]
                appendColumns(operation, columns)

        # Dividir las operaciones dentro de parentesis

        if char == '(':
            if proposition[i + 1] != '(' and proposition[i - 1] != '(':
                closingParenthesis = proposition.find(')', i)
                operation = proposition[i:closingParenthesis + 1]
                appendColumns(operation, columns)
            elif i < len(proposition) - 1 and proposition[i + 1] == '(':
                closingParenthesis = proposition.find(')', i)
                operation = proposition[i + 1:closingParenthesis + 1]
                appendColumns(operation, columns)
                closingParenthesis = proposition.find(')', closingParenthesis + 1)
                operation = proposition[i + 1:closingParenthesis + 1]
                appendColumns(operation, columns)

    # Añadir la proposicion completa

    appendColumns(proposition, columns)

# Añadir operacion dividida filtrando los registros duplicados

def appendColumns(operation, columns):
    duplicate = False
    for column in columns:
        if operation.strip('()') == column.strip('()'):
            duplicate = True
    if not duplicate:
        columns.append(operation)

