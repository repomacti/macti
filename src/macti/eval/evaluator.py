"""
@author: Luis M. de la Cruz [Updated on Mon Aug 25 09:30:10 CST 2025].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
import math
import numpy as np
import pandas as pd
import sympy as sy
import os, sys, platform

#import pkg_resources
from IPython.display import display, Latex
        
class Quiz():
    def __init__(self, qnum, course, server = 'hub', spath = ''):
        """
        Clase para la evaluación de ejercicios.
        
        Parameters
        ----------
        qnum : str
            Nombre del quiz.

        course : str
            Nombre del directorio del curso.
        
        server : str
            Puede tener cualquiera de los dos siguientes valores:
            'local' cuando los datos (answers & feedback) se almacenan en un directorio local.
            'hub' cuando los datos (answers & feedback) se almacenan en un directorio global del hub.

        spath : str
            Directorio de intercambio de nbgrader. Cuando server = 'hub' esta ruta se debe proporcionar.
        """
        self.__server = server

        cp, to = os.path.split(os.getcwd()) # Extracción del path del curso y del tema

        # Construcción del path para los archivos de respuestas
        if self.__server == 'local':
            self.__ans_path = os.path.join(cp, ".ans", to)
        elif self.__server == 'hub':
            #_, cn = os.path.split(cp)
            cn = course
            self.__server_path = "/usr/local/share/nbgrader/exchange/" # Ruta en MACTI
            self.__ans_path = os.path.join(self.__server_path, cn, ".ans", to)
        
        self.__quiz_num = qnum # Número del quiz

        # Verbosity
        self.__verb = self.__read('0', verb = True)['0'][0]

        self.__line_len = 40
        self.__line = 40 * chr(0x2015)

    @property
    def verb(self):
        return self.__verb
        
    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def __read(self, enum, name = '.__ans_', verb = False):
        """
        Lectura de la respuesta del ejercicio con número enum. 
        
        Esta lectura se realiza del archivo en donde se encuentran las respuestas de todo el quiz.
        El archivo está en formato parquet y las respuestas se almacenan en columnas y en un solo renglón.
        El identificador de la columna corresponde con el número del ejercicio enum.

        Parameters
        ----------
        enum: str
            Número del ejercicio dentro del quiz.
        
        name: string
            Nombre del archivo donde se guardan las respuestas, por omisión es: ".__ans_".

        verb: bool
            Es False siempre, excepto cuando se lee la verbosidad.
        
        Returns
        -------
            Regresa la respuesta correcta al ejercicio enum almacenada en el archivo.
        """
        try:
            # Solo se permite enum == '0' cuando se lee la verbosidad (verb == True)
            if enum == '0' and not verb:
                raise ValueError from None

        except ValueError:
            print('NO EXISTE LA RESPUESTA. No está permitido usar \'{}\' para identificar un ejercicio \n'.format(enum))
        else:   
            # Se agrega el número del quiz correspondiente al nombre del archivo de respuestas. 
            filename = name + self.__quiz_num
            stream = os.path.join(self.__ans_path, filename)

            # Lectura del archivo en formato parquet, se regresa en un DataFrame.
            # Solo se lee la columna correspondiente con el identificador 'enum'
            return (pd.read_parquet(stream, columns=[enum]))

    def __print_correct(self, enum, equiz="", ans=""):
        """
        Imprime el mensaje cuando la respuesta es correcta.

        Parameters
        ----------
        enum : str
            Número del ejercicio dentro del quiz.      

        equiz : str
            Tipo de evaluación.
        """
        print(Fore.RESET + self.__line)
        if equiz == "option":
            print(Fore.GREEN + enum + ' | Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.GREEN + ', es correcta.') 
        elif equiz == "expression":
            print(Fore.GREEN + enum + ' | Tu respuesta:')
            display(ans)
            print(Fore.GREEN + 'es correcta.')
        else:
            print(Fore.GREEN + enum + ' | Tu resultado es correcto.')
        print(Fore.RESET + self.__line)
    
    def __print_error_hint(self, enum, equiz="", ans="", msg="", info=""):
        """
        Imprime el mensaje cuando hay un error y la retroalimentación.

        Parameters
        ----------
        enum : str
            Número del ejercicio dentro del quiz.

        equiz : str
            Tipo de evaluación.
            
        msg : str
            Mensaje con el posible error encontrado.
        """
        print(Fore.RESET + self.__line)
        if equiz == "option":
            print(Fore.RED + enum + ' | Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.RED + ', es INCORRECTA.') 
        elif equiz == "expression":
            print(Fore.RED + enum + ' | Tu respuesta:')
            display(ans)
            print(Fore.RED + 'NO es correcta.')
        else:
            print(Fore.RED + enum + ' | Ocurrió un error en tus cálculos.')
        print(Fore.RESET + self.__line)
        print(Fore.RED + 'Hint:', end = ' ')
    
        # Se obtiene la retroalimentación para la pregunta correspondiente.            
        feedback = self.__read(enum, '.__fee_')
        
        # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
        # En otro caso no se imprime nada.
        if feedback[enum][0] != None and self.__verb >= 1:            
            print(Fore.RED + feedback[enum][0] + msg)
        else:
            print()            
            print(Fore.RESET + self.__line)
            
        # Se imprime la información del error.
        if self.__verb >= 2:
            print(info)

    def __test_string_array(self, b, a):
        """
        Compara dos arreglos de valores tipo cadena (str).
        
        Para comparar la respuesta del alumno (b) con la respuesta correcta (a) 
        debemos usar la función flatten(), para que ambos arreglos sean lineales (1D).
        Utilizamos la función np.allcose() para comparar los arreglos elemento por elemento
        dentro de una tolerancia definida (rtol=1e-05, atol=1e-08). Si hay NaN´s en los arreglos
        la función devuelve True si están en el mismo lugar dentro de los arreglos.

        Parameters
        ----------
        a : ndarray
            Respuesta correcta.

        b : ndarray
            Respuesta del alumno.

        Returns
        -------
        msg : str
            Mensaje con el posible error encontrado: 
             - diferencia entre longitudes de los arreglos.
             - diferencia en algún elemento de los arreglos (la primera que ocurre).
        """
        b = b.flatten()
        msg = ""
        if len(a) == len(b):
            first = np.where((a == b) == False)[0]
            msg = f"\n Lugares donde hay diferencia: {first}"
                    
        else:
            # Cuando la longitud de los arreglos es distinta
            msg = f"\nLongitud correcta={len(a)}\nLongitud de tu respuesta={len(b)}"
                
        return msg
        
    def __test_numeric_array(self, b, a):
        """
        Compara dos arreglos de valores numéricos.
        
        Para comparar la respuesta del alumno (b) con la respuesta correcta (a) 
        debemos usar la función flatten(), para que ambos arreglos sean lineales (1D).
        Utilizamos la función np.allcose() para comparar los arreglos elemento por elemento
        dentro de una tolerancia definida (rtol=1e-05, atol=1e-08). Si hay NaN´s en los arreglos
        la función devuelve True si están en el mismo lugar dentro de los arreglos.

        Parameters
        ----------
        a : ndarray
            Respuesta correcta.

        b : ndarray
            Respuesta del alumno.

        Returns
        -------
        msg : str
            Mensaje con el posible error encontrado: 
             - diferencia entre longitudes de los arreglos.
             - diferencia en algún elemento de los arreglos (la primera que ocurre).
        """
        b = b.flatten()
        msg = ""
        if len(a) == len(b):
            if not np.allclose(a, b, equal_nan=True):
                first = np.where((a == b) == False)[0]
                msg = f"\n Lugares donde hay diferencia: {first}"    
        else:
            # Cuando la longitud de los arreglos es distinta
            msg = f"\nLongitud correcta={len(a)}\nLongitud de tu respuesta={len(b)}"
                
        return msg
        
    def eval_option(self, enum, ans):
        """
        Evalúa una pregunta de opción múltiple. 
        
        Cuando la respuesta es incorrecta lanza un excepción.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo.
        answer = self.__read(enum)
        # Eliminamos espacios que haya de más en la respuesta del alumno.
        ans = ans.replace(" ","") 

        # Se compara la respuesta del alumno (ans) con la correcta (answer[enum][0])
        # La comparación se realiza en minúsculas.
        correct = ans.lower() == answer[enum][0].lower()
        
        if correct:
            self.__print_correct(enum, equiz="option", ans=ans)
        else:
            self.__print_error_hint(enum, equiz="option", ans=ans)

            # Se lanza una excepción con la información correspondiente.
            raise AssertionError from None

    def eval_expression(self, enum, ans):
        """
        Evalúa una expresión simbólica escrita en formato Python+Sympy.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo.
        value = self.__read(enum)

        # Se convierte la respuesta correcta (value) en formato SymPy.
        correct = sy.sympify(value[enum][0])

        # Se compara la respuesta correcta (correct) con la respuesta
        # del alumno (ans) usando la función equals().
        if correct.equals(ans):
            self.__print_correct(enum, equiz="expression", ans=ans)
        else:
            self.__print_error_hint(enum, equiz="expression", ans=ans)

            # Se lanza una excepción con la información correspondiente.
            raise AssertionError from None

    def eval_numeric(self, enum, ans):
        """
        Evalúa una respuesta numérica que puede ser un número o un arreglo de números.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo. Recordemos que
        # Parquet escribe listas y tuplas en forma de np.ndarray, por lo que
        # al recuperarlas del archivo vienen en formato np.ndarray en 1D.
        value = self.__read(enum)        
        correct = value[enum][0]
        msg = ""

        try:
            if isinstance(ans, np.ndarray):
                if ans.dtype == complex:
                    # Preprocesamiento especial para números complejos.
                    b = np.array([[c.real, c.imag] for c in ans.flatten()]).flatten()
                    msg = self.__test_numeric_array(b, correct)
                    np.testing.assert_allclose(b, correct)                  
                else:                        
                    msg = self.__test_numeric_array(ans, correct)
                    np.testing.assert_allclose(ans, correct)

            elif isinstance(ans, list) or isinstance(ans, tuple):
                b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                msg = self.__test_numeric_array(b, correct)
                np.testing.assert_allclose(b, correct)

            elif isinstance(ans, set):
                b = np.array(list(ans))
                msg = self.__test_numeric_array(b, correct)
                np.testing.assert_allclose(b, correct)

            elif isinstance(ans, complex):
                a = complex(correct[0], correct[1])
                b = np.array([ans.real, ans.imag])
                
                if not np.allclose(correct, b):
                    msg = f"\n Valor correcto  : {a}\n Valor calculado : {ans}\n"
                    raise AssertionError from None

            elif isinstance(ans, int) or isinstance(ans, float) or isinstance(ans, bool):
                if not math.isclose(correct, ans):
                    msg = f"\n Valor correcto  : {correct}\n Valor calculado : {ans}\n"
                    raise AssertionError from None

            else:
                print(enum + ' | Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg, info=info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
        else:
            self.__print_correct(enum)

    def eval_datastruct(self, enum, ans, in_order=True):
        """
        Evalúa una respuesta almacenada en una estructura de datos.
        
        Parameters
        ----------
        enum: string
            Número de pregunta.
        
        ans: string
            Respuesta del alumno.

        in_order: bool
            Si la respuesta debe estar en orden (True) o no (False).
        """
        # Se obtiene la respuesta correcta del archivo. Recordemos que
        # Parquet escribe listas y tuplas en forma de np.ndarray, por lo que
        # al recuperarlas del archivo vienen en formato np.ndarray en 1D.
        value = self.__read(enum)        
        correct = value[enum][0]
        msg = ""       

        try:
            if isinstance(ans, set) or isinstance(ans, tuple): 
                ans = list(ans)
                
            if isinstance(ans, list):
                if in_order: 
                    b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                    msg = self.__test_string_array(b, correct)
                    np.testing.assert_equal(b, correct)
                else:
                    b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                    b.sort()
                    correct.sort()
                    msg = self.__test_string_array(b, correct)
                    np.testing.assert_equal(b, correct)                    
                    
            else:
                print('Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
            
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg, info=info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
        else:
            self.__print_correct(enum)
            
    def eval_dict(self, enum, ans, numeric = True):
        """
        Evalúa una respuesta almacenada en un diccionario.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.

        numeric: bool.
            Verifica
        """
        enum_copy = enum
        msg = ""       
        
        try:
            if isinstance(ans, dict):
                # Se obtiene la longitud del diccionario y se compara con la respuesta del alumno.
                dict_len = len(ans) # Respuesta del alumno
                enum = enum_copy + "_len" # etiqueta de la columna con la respuesta en el archivo
                value = self.__read(enum)   
                correct = value[enum][0]
                if not math.isclose(correct, dict_len):
                    msg = f"\n Valor correcto  : {correct}\n Valor calculado : {dict_len}\n"
                    raise AssertionError from None
                
                # Se obtienen los keys del diccionario y se comparan con la respuesta del alumno.
                keys = np.array(list(ans.keys())) # Respuesta del alumno
                enum = enum_copy + "_key" # etiqueta de la columna con la respuesta en el archivo
                value = self.__read(enum)        
                correct = value[enum][0]
                where = np.where((correct == keys) == False)
                if len(where[0]) > 0:
                    msg = f"\n Keys correctas  : {correct}\n Keys calculadas : {keys}\n"
                    np.testing.assert_equal(keys, correct)

                # Se obtienen los valores del diccionario, uno a uno, y se comparan con la respuesta del alumno.
                for i, b in enumerate(ans.values()):
                    enum = enum_copy + "_val_" + str(i)
                    value = self.__read(enum)        
                    correct = value[enum][0]

                    if numeric:
                        if isinstance(b, int) or isinstance(b, float) or isinstance(b, bool):
                            if not math.isclose(correct, b):
                                msg = f"\n Valor correcto  : {correct}\n Valor calculado : {b}\n"
                                raise AssertionError from None
                                
                        elif isinstance(b, list) or isinstance(b, tuple) or isinstance(b, set):
                            if isinstance(ans, set): ans = list(ans)
                            b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                            msg = self.__test_numeric_array(b, correct)
                            np.testing.assert_allclose(b, correct)    
                    else:
                        if isinstance(b, str):
                            if correct != b:
                                msg = f"\n Valor correcto  : {correct}\n Valor calculado : {b}\n"
                                raise AssertionError from None
                                
                        elif isinstance(b, list) or isinstance(b, tuple) or isinstance(b, set):
                            if isinstance(ans, set): ans = list(ans)
                            b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                            msg = self.__test_string_array(b, correct)
                            np.testing.assert_equal(b, correct)   

            else:
                print(enum + ' | Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg,  info=info)
            
            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None

        else:
            self.__print_correct(enum) 
            




    

