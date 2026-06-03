"""
@author: Luis M. de la Cruz [Tue Jun  2 17:55:18     2026].
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

class FileAnswer():
    def __init__(self):
        """
        Clase para la escritura de las respuestas a los ejercicios.
        
        Se asume que se ejecuta dentro del directorio de un tema del curso
        por ejemplo course/topic.
        
        Los datos (answers & feedback) se almacenan en el directorio:.
        $PWD/course/.ans/topic/. 
        
        Las respuestas/retroalimentación para cada quiz 
        se almacenan en archivos diferentes, veáse la función to_file().
        """
     
        # Extracción del path del curso y del tema: cp=course path, to = topic
        cp, to = os.path.split(os.getcwd()) 
        # Construcción del path del directorio para los archivos de respuestas
        self.__ans_path = os.path.join(cp, ".ans", to) # cp/.ans/to

        # Listas para almacenar los números de las respuestas, las respuestas
        # y la retroalimentación.
        self.__exernum = []
        self.__answers = []
        self.__feedback = []

        # Por omisión la verbosidad es igual a 2, es decir toda la ayuda posible al alumno
        self.__verb = 2

        # Cadena final del nombre de los archivos, se actualiza en la función self.to_file()
        self.__quiz_num = ""

    @property
    def quiz_num(self):
        return self.__quiz_num
        
    @property
    def answers(self):
        return self.__answers
    
    @property
    def feedback(self):
        return self.__feedback

    @property
    def verb(self):
        return self.__verb
        
    @verb.setter
    def verb(self, verb):
        self.__verb = verb
             
    def write(self, enum, ans, feed=None, verb = False):
        """
        Escribe la respuesta y la retroalimentación de una pregunta.
        
        Esta función escribe una respuesta en una lista (self.__answers) y la retroalimentación de 
        esta respuesta en otra lista (self.__feedback). El número del ejercicio se almacena en 
        otra lista (self.__exernum). Si la respuesta es nueva, se agrega un elemento a la lista, 
        si el ejercicio ya existía entonces se sustituye.

        Parameters
        ----------
        enum: str
            Cadena con el identificador del ejercicio. Este parámetro no puede ser '0' debido
            a que ese identificador está destinado a almacenar la verbosidad de la retroalimentación.

        ans: str, float, int, complex, boolean, ndarray, list, tuple, dict
            Objeto que contiene la respuesta, puede ser de cualquier tipo soportado por la
            biblioteca (str, float, int, complex, boolean, ndarray, list, tuple, dict)

        feed: str
            Cadena con la retroalimentación del ejercicio. Por omisión está vacía.

        verb: bool
            Es False siempre, excepto cuando se escribe la verbosidad.
        """
        try:
            # Solo se permite enum == '0' cuando se almacena la verbosidad (verb == True)
            if enum == '0' and not verb:
                raise ValueError from None

        except ValueError:
            print('RESPUESTA NO ALMACENADA. No está permitido usar el valor \'{}\' para identificar un ejercicio.\n'.format(enum))
            
        else:
            # Sustitución de una respuesta y de su retroalimentación
            if enum in self.__exernum: # checamos si ya existe el número de ejercicio
                
                index = self.__exernum.index(enum) # obtenemos el índice en la lista

                # Dependiendo del tipo de dato de la respuesta, la almacenamos de manera distinta
                #
                # ndarray
                if isinstance(ans, np.ndarray):
                    if ans.dtype == complex:
                        # Preprocesamiento especial para números complejos.
                        self.__answers[index] = np.array([[c.real, c.imag] for c in ans.flatten()]).flatten()
                    else:
                        self.__answers[index] = ans.flatten() # almacenamos los arreglos de numpy en 1D
                #
                # dict
                elif isinstance(ans, dict):
                    # Extraemos cada key y value del diccionario y almacenamos en 
                    # columnas separadas lo siguiente:
                    # - La longitud del diccionario
                    # - Las keys como un arreglo
                    # - Cada value como un arreglo
                    dict_len = len(ans)
                    keys = np.array(list(ans.keys()))
                    enum_l = enum + "_len"
                    enum_k = enum + "_key"

                    # Recursión para almacenar la longitud y keys:values del diccionario por separado 
                    # Escribimos la longitud del diccionario
                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    # Escribimos la lista de claves
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")
                    # Escribimos cada valor
                    for i, v in enumerate(ans.values()):
                        enum_v = enum + "_val_" + str(i)        
                        self.write(enum_v, v, f"{feed}. \n{enum_v} Valor en el diccionario incorrecto.")
                #
                # set
                elif isinstance(ans, set):
                    self.__answers[index] = np.array(list(ans)).flatten()
                #
                # list o tuple
                elif isinstance(ans, list) or isinstance(ans, tuple):
                    self.__answers[index] = np.array(ans).flatten()
                #
                # complex
                elif isinstance(ans, complex):
                    # Almacenamos la parte real e imaginaria del número complejo en una lista.
                    self.__answers[index] = [ans.real, ans.imag]
                #
                # Cualquier otro caso: str, int, float
                else:
                    self.__answers[index] = ans
                #
                # Almacenamos la retroalimentación
                self.__feedback[index] = feed 
                
            else: # Si el ejercicio es nuevo, lo agregamos

                # Dependiendo del tipo de dato de la respuesta, la almacenamos de manera distinta
                #
                # ndarray
                # Todos los arreglos de numpy se deben almacenar en formato unidimensional
                if isinstance(ans, np.ndarray):
                    if ans.dtype == complex:
                        # Preprocesamiento especial para números complejos.
                        self.__answers.append(np.array([[c.real, c.imag] for c in ans.flatten()]).flatten())
                    else:
                        self.__answers.append(ans.flatten()) # almacenamos los arreglos de numpy en 1D   
                #
                # dict
                elif isinstance(ans, dict): 
                    # Extraemos cada key y value del diccionario y almacenamos en 
                    # columnas separadas lo siguiente:
                    # - La longitud del diccionario
                    # - Las keys como un arreglo
                    # - Cada valueo como un arreglo
                    dict_len = len(ans)
                    keys = np.array(list(ans.keys()))
                    enum_l = enum + "_len"
                    enum_k = enum + "_key"

                    # Escribimos la longitud del diccionario
                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    # Escribimos la lista de claves
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")
                    # Escribimos cada valor
                    for i, v in enumerate(ans.values()):
                        enum_v = enum + "_val_" + str(i)        
                        self.write(enum_v, v, f"{feed}. \n{enum_v} Valor en el diccionario incorrecto.")
                #
                # set
                elif isinstance(ans, set):
                    self.__answers.append(np.array(list(ans)).flatten())
                #
                # list o tuple
                elif isinstance(ans, list) or isinstance(ans, tuple):
                    self.__answers.append(np.array(ans).flatten())
                #
                # complex
                elif isinstance(ans, complex):
                    # Parquet no soporta complejos, dividimos en parte real e imaginaria
                    self.__answers.append([ans.real, ans.imag])    
                #
                # Cualquier otro caso: str, int, float               
                else:
                    self.__answers.append(ans)

                if not isinstance(ans, dict): # El caso de diccionarios los números de pregunta y la retroalimentación se
                                              # almacenan de forma diferente. Véase la primera opción del 'if'
                    self.__exernum.append(enum)  # Se almacena el número de la pregunta
                    self.__feedback.append(feed) # Se almacena la retroalimentación de la pregunta
    
    def to_file(self, qnum):
        """
        Escribe las respuestas y la retroalimentación en un archivo tipo parquet.

        Parameters
        ----------
        qnum: str
            Es una cadena que identifica a una pregunta del quiz. 
            Se recomienta usar: '1', '2', ...
        """
        # Cadena final del nombre de los archivos de respuestas y de retroalimentación
        self.__quiz_num = qnum
        
        # Se define la verbosidad de la retroalimentación de cada respuesta. 
        self.write('0', self.__verb, verb = True)
        
        if not os.path.exists(self.__ans_path):
            print('Creando el directorio :{}'.format(self.__ans_path))
            os.makedirs(self.__ans_path, exist_ok=True)
        else:
            print('El directorio :{} ya existe'.format(self.__ans_path))

        # Creación del archivo de respuestas
        ans_df = pd.DataFrame([self.__answers], columns=self.__exernum)
        ans_filename = os.path.join(self.__ans_path, '.__ans_' + qnum)
        # Escritura de las respuestas en formato parquet
        ans_df.to_parquet(ans_filename, compression='gzip')

        # Creación del archivo de retroalimentación
        feed_df = pd.DataFrame([self.__feedback], columns=self.__exernum) 
        feed_filename = os.path.join(self.__ans_path, '.__fee_' + qnum)
        # Escritura de la retroalimentación en formato parquet
        feed_df.to_parquet(feed_filename, compression='gzip')
        
        print('Respuestas y retroalimentación almacenadas.')

        