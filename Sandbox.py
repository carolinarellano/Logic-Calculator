#Used to practice and check the functions

from Operators import and_function

prueba = ['p', 'q', 'r', '(p→q)', '(p→q)∧r']

proposition = {
  'p': ['V', 'V', 'F', 'F'], 
  'q': ['V', 'F', 'V', 'F']
}

def FuncionLuis(proposition):
  return 'ArregloDividido'

def funcionArlyn(funcionLuis):
  return 'Dictionary'

def FuncionCaro(funcionLuis, funcinoArlyn):
  return 'TabladeVerdad'

# print(and_function('p∧q', proposition['p'], proposition['q']))

