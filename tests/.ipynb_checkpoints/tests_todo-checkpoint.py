#----------------------- TEST OF THE MODULE ----------------------------------   

from macti.eval import FileAnswer
from macti.eval import Quizz

import numpy as np
import pandas as pd
import sympy as sy

def tests():
    #----- CREACIÓN DE RESPUESTAS
    opcion = 'c'
    
    # Símbolos de sympy para cálculo simbólico
    x = sy.Symbol('x')
    y = sy.Symbol('y')
    
    # Función simbólica
    derivada = x*x
    
    # Forma cuadrática
    matriz_np = np.array([[0.10, -1.],[0.30,-1.]] )
    array_np = np.array([-200, 20])
    A, B, C = matriz_np, array_np, 0.0
    forma_cuadratica = 0.5 * A[0,0] * x**2 + 0.5 * A[1,1] * y**2 + 0.5 * (A[0,1]+A[1,0])* x * y - B[0] * x - B[1] * y + C

    # Datos básicos
    flotante = 0.1
    entero = 1
    logico = True
    complejo = 1 + 5j

    # Estructuras de datos
    lista_num = [0, 1, 3.4]
    lista = ['luis', 'miguel', 'delacruz']

    tupla_num = (1.2, 3.1416, np.pi)
    tupla = ('a', 'b', 'c')

    conjunto_num = {1, 3, 2, 6, 5, 4}
    conjunto = {'a', 'b', 'c'}
    
    diccionario_num = {1:3.446, 2:5.6423, 3:2.234324}
    diccionario_k_str = {'k1':1, 'k2':2, 'k3':3}
    diccionario_kv_str= {'k1':'luis', 'k2':'miguel', 'k3':'x'}

    # Arreglos de numpy
    w = np.sin(np.linspace(0,1,10))
    arreglo_complejo = np.array([1j,2j,3j,4j,5j])

    # Estructuras de datos más complejas
    lista_lista = [[1,2],[3,4]]

    # Lista y tuplas no ordenadas
    lista_no = ['a', 'b', 'x', '4', 'c']
    tupla_no = ('a', 'b', 'x', '4', 'c')

    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 3:[2.234324, 5.65645]}

    #----- CREACIÓN DEL DATAFRAME DE RESPUESTAS
    
    print("Iniciamos con FileAnswer")
    file_answer = FileAnswer()
#    file_answer.verb = 0 # Se puede cambiar la verbosidad, por omisión es igual 2
    file_answer.write('0', 'a', 'Opción inválida')
    file_answer.write('1', opcion, 'Las opciones válidas son ...')
    
    # OJO: las expresiones de sympy se deben convertir en 'str' antes de escribirse en el archivo
    file_answer.write('2', str(derivada), 'Checa las reglas de derivación')
    file_answer.write('3', str(forma_cuadratica),'Revisa tus operaciones algebráicas para calcular f(x)')

    file_answer.write('4', flotante, 'Checa el valor de flotante')
    file_answer.write('5', entero, 'Checa el valor de entero')
    file_answer.write('6', logico, 'Checa  logico')
    file_answer.write('7', complejo, 'Checa el valor de complejo')

    file_answer.write('8', lista_num, 'Checa la lista numérica')
    file_answer.write('9', lista, "checa la estructura de tipo lista")

    file_answer.write('10', tupla_num, 'Checa la tupla numérica')
    file_answer.write('11', tupla, "checa la estructura de tipo tupla")

    file_answer.write('12', conjunto_num, 'Checa los conjuntos numéricos')
    file_answer.write('13', conjunto, "checa la estructura de tipo conjunto")

    file_answer.write('14', diccionario_num, 'Checa los diccionarios numéricos')
    file_answer.write('15', diccionario_k_str, 'Checa los diccionarios con keys str')
    file_answer.write('16', diccionario_kv_str, "checa la estructura de tipo diccionario")
    
    mensaje ="""Puedes poner mucho texto y ver que sucede en la impresión del hint,
    quizá es necesario usar triples comillas"""
    file_answer.write('17', w, mensaje)
    file_answer.write('18', arreglo_complejo, 'Checa el arreglo complejo')

    file_answer.write('19', lista_lista, "Checa la lista de listas")
    file_answer.write('20', lista_no, "Checa la lista NO ordenada")
    file_answer.write('21', tupla_no, "Checa la tupla NO ordenada")

#    file_answer.write('21', diccionario_num_list, 'Checa los diccionarios numéricos con valores tipo lista')

    #----- ESCRITURA DE LAS RESPUESTAS Y LA RETROALIMENTACIÓN ARCHIVOS.
    
    file_answer.to_file('test01')

    #----- MOSTRAMOS LOS ARCHIVO DE RESPUESTAS Y DE RETROALIMENTACIÓN
    
    ans = pd.read_parquet('../.ans/eval/.__ans_test01')
    fee = pd.read_parquet('../.ans/eval/.__fee_test01')
    print("\n----- RESPUESTAS Y DE RETROALIMENTACIÓN")
    fstr = "Pregunta {}:\n a --> {}\n f --> {}\n"
    [print(fstr.format(i, ans[i][0], fee[i][0])) for i in ans.columns]

#    print(len(file_answer.answers), "\n", file_answer.answers)
#    print()
#    print(len(file_answer.feedback), "\n", file_answer.feedback)

    #----- CREACIÓN DE LAS EVALUACIONES
    
    print("Quiz number:", file_answer.quiz_num)

    quiz = Quiz(file_answer.quiz_num, 'macti', 'local')
#    quiz2 = Quiz(file_answer.quiz_num, 'macti')
    
    print('\nVerbosidad de la ayuda : {} \n'.format(quiz.verb))
    
    print('Opción')
    quiz.eval_option('1', opcion)
    
    print('Expresión')
    quiz.eval_expression('2', derivada)

    print('Expresión más compleja')
    quiz.eval_expression('3', forma_cuadratica)
    
    print('Flotante')
    quiz.eval_numeric('4', flotante)
    
    print('Entero')
    quiz.eval_numeric('5', entero)
    
    print('Logico')
    quiz.eval_numeric('6', logico)

    print('Complejo')
    quiz.eval_numeric('7', complejo)

    print('Lista numérica')
#    lista_num = [0, 1]
#    lista_num[-2] =0.001
    quiz.eval_numeric('8', lista_num)

    print('Lista')
#    lista = ['miguel', 'delacruz']
#    lista = ['luis', 'migul', 'delacruz']
    quiz.eval_datastruct('9', lista)

    print('Tupla numérica')
#    tupla_num = (0, 1)
#    tupla_num = (1.2, 3.1416, 2*np.pi)
    quiz.eval_numeric('10', tupla_num)    

    print('Tupla')
#    tupla = ('a', 'b')
#    tupla = ('a', 'd', 'c')
    quiz.eval_datastruct('11', tupla)  
    
    print('Conjunto numérico')
#    conjunto_num = {1,2,3,4,5,1}
#    conjunto_num = {1,2,3.5,4,5,6}
    quiz.eval_numeric('12', conjunto_num)

    print('Conjunto')
#    conjunto = {'a', 'b'}
#    conjunto = {'a', 'b', 'x'}
    quiz.eval_datastruct('13', conjunto)
    
    print('Diccionario numérico')
#    diccionario_num = {1:3.446, 2:5.6423}
#    diccionario_num = {1:3.44, 4:5.6423, 3:2.234324}
#    diccionario_num = {1:3.446, 2:5.642, 3:2.234324}
    quiz.eval_dict('14', diccionario_num)

    print('Diccionario con keys str y values numéricos')
#    diccionario_k_str = {'k1':1, 'k2':2}
#    diccionario_k_str = {'k1':1, 'k4':2, 'k3':3}
#    diccionario_k_str = {'k1':1, 'k2':2.4, 'k3':3}
    quiz.eval_dict('15', diccionario_k_str)

    print('Diccionario con keys y values str')
#    diccionario_kv_str= {'k1':'luis', 'k2':'miguel'}
#    diccionario_kv_str= {'k1':'luis', 'k4':'miguel', 'k3':'x'}
#    diccionario_kv_str= {'k1':'luis', 'k2':'mil', 'k3':'x'}
    quiz.eval_dict('16', diccionario_kv_str, numeric = False)

    print('numpy array')
#    w = np.sin(np.linspace(0,1,5))
#    w[2:4] = 4.5
    quiz.eval_numeric('17', w)

    print('numpy array complex')
#    arreglo_complejo = np.array([2j,3j,4j,5j])
#    arreglo_complejo = np.array([0j,2j,3j,4j,5j])
    quiz.eval_numeric('18', arreglo_complejo)

    print('Lista de listas')
#    lista_lista = [[1,2],[3,4],[5,6]]
#    lista_lista = [[1,2],[3.14,4]]
    quiz.eval_numeric('19', lista_lista)

    print('Lista NO ordenada')
    # Lista original: lista_no = ['a', 'b', 'x', '4', 'c']
    # La respuesta puede estar en otro orden y ser correcta
#    lista_no = ['x', '4', 'a', 'c', 'b']
    # Los siguientes casos fallan
#    lista_no = ['x', '4', 'c', 'b']
#    lista_no = ['x', '4', 'c', 'b', 'y']
    quiz.eval_datastruct('20', lista_no, in_order=False)

    print('Tupla NO ordenada')
    # Tupla original: tupla_no = ('a', 'b', 'x', '4', 'c')
    # La respuesta puede estar en otro orden y ser correcta
#    tupla_no = ('x', '4', 'a', 'c', 'b')
    # Los siguientes casos fallan
#    tupla_no = ('x', '4', 'c', 'b')
#    tupla_no = ('x', '4', 'c', 'b', 'y')
    quiz.eval_datastruct('21', tupla_no, in_order=False)
    
#    print('Diccionario numérico con valores tipo lista')
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 5:[2.234324, 5.65645]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.643, 6.7564], 3:[2.234324, 5.65645]}
#    quiz.eval_dict('22', diccionario_num_list)


tests()