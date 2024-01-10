#
# Author: Luis Miguel de la Cruz Salas
# Last update: Wed Aug 30 08:56:42 PM UTC 2023
#
import os, sys, shutil, pkg_resources
import pandas as pd

# Definición de las rutas
home = os.environ['HOME'] + '/'
path = os.getcwd() + '/'

# Se determina si el curso es nuevo o se actualizará uno ya existente
new_update = input('\n ¿Curso nuevo [N] o actualización [A]? ')
if new_update in ['N', 'n']:
    # Lista de temas para el curso
    topic_list = pd.read_csv('topics_course_create.csv')
elif new_update in ['A','a']:
    # Lista de temas nuevos para el curso
    topic_list = pd.read_csv('topics_course_update.csv')
else:
    sys.exit(' ERROR: Opción incorrecta: {}'.format(new_update))

# Se genera el nombre del curso
c_name = input('\n Nombre del curso : ')
c_path = path + c_name + '/'

# Se crea el directorio del curso, se revisa antes si ya existe
if not os.path.exists(c_name):
    if new_update in ['N', 'n']:
        print('\n ---> Creando el directorio : {}'.format(c_path))
        os.makedirs(c_path , exist_ok=True)
    else:
        print(' ERROR: El curso "{}" no existe, checa el nombre correcto.'.format(c_name))
        sys.exit('Termina el proceso anticipandamente')
else:
    if new_update in ['A', 'a']:
        print(' Directorio del curso: {}'.format(c_path))
    else:
        print(' ERROR: El curso "{}" ya existe.'.format(c_name))
        sys.exit('Termina el proceso anticipandamente')        

# Se determina de donde se van a copiar los archivos
src_dir = input(' Directorio de los fuentes ("macti_notes/notebooks/" <enter>):')

if src_dir in ['']:
    src_dir = 'macti_notes'
else:
    pass
src_dir_path = path + src_dir + '/'
print(' {}'.format(src_dir_path))

# Antes de continuar se pregunta si todo está correcto para continuar
seguro = input("\n Se copiara información de '{}' a '{}', \n ¿continuar? Si [S], No [N]' ".format(src_dir_path, c_path))

if seguro in ['S', 's']:
    pass
else:
    sys.exit('Termina el proceso anticipandamente.')        

# No hay vuelta atrás, se hace la copia, sobreescribiendo si es necesario.
print("\n -- Copiando información de '{}' a '{}' ".format(src_dir_path, c_path))

# Copiamos las notebooks correspondientes al directorio del curso.
for topic in topic_list:
    
    # Se crea el subdirectorio del tema
    p = c_path + topic
    if not os.path.exists(p):
        print('\n ---> Creando el directorio : {}'.format(p))
        os.makedirs(p , exist_ok=True)
    else:
        print(' Subdirectorio del tema: {}'.format(p))
    
    # Se copian los archivos al subdirectorio del tema
    for a in topic_list[topic]:
        if not isinstance(a, float):
            
            # Subdirectorio fuente
            if src_dir == 'macti_notes':
                src = src_dir_path + 'notebooks/' + topic + '/' + a
            else:
                src = src_dir_path + topic + '/' + a
            
            # Subdirectorio destino
            dst = c_path + topic   
            print(' Fuente: {} \n Destino: {}\n'.format(src, dst))
            shutil.copy2(src, dst)