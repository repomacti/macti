import os, shutil
from colorama import Fore, Back, Style

def print_macti_info(msg):
    print(Fore.GREEN + '[MACTI | INFO] ' + Style.RESET_ALL, end = '')
    print(Back.WHITE + ' --> ' + msg + Style.RESET_ALL, end='\n')

os.system('clear')

line_len = 50
print()
print(Fore.WHITE + Back.GREEN + line_len*'-')
print(Fore.WHITE + Back.GREEN + '    MACTI: Creación del repositorio del curso     ' + Style.RESET_ALL)
print(Fore.WHITE + Back.GREEN +  line_len*'-')
print(Style.RESET_ALL)

c_name = input(' Nombre del curso : ')
print()

path = os.getcwd()
paths = [c_name + '/Tema1/', 
         c_name + '/.ans/',
        ]

for p in paths:
    if not os.path.exists(p):
        print_macti_info('Creando el directorio : {}  '.format(p))
        os.makedirs(p , exist_ok=True)
    else:
        print_macti_info('El directorio : {} ya existe  '.format(p))

print_macti_info('Cambiando al directorio : {}  '.format(path + '/' + c_name))
os.chdir(c_name)

print_macti_info('Iniciando el repositorio  ')
os.system('git init')

lines = []
lines.append("# NBGRADER \n")
lines.append("nbg \n\n")
lines.append("# QUIZ \n")
lines.append("q*.ipynb \n")
lines.append(".ans/ \n")

print_macti_info('Creando ' + Style.BRIGHT + '.gitignore ')
with open(".gitignore", "w") as f:
    f.writelines(lines)

print_macti_info('Estado del repositorio  (git status)')
os.system('git status')
print_macti_info('Actualizando los cambios (git add .) ')
os.system('git add .')
os.system('git status')
print_macti_info('Confirmando los cambios (git commit -m " ... ")')
os.system('git commit -m "Iniciando el repositorio"')
print_macti_info('Estado del repositorio  (git status)')
os.system('git status')


#for i in range(1,4):
#    filename = '/data/Plantillas/plantilla0' + str(i) + '.ipynb'
#    stream = pkg_resources.resource_stream('macti', filename)
#    print('Copiando {} al directorio {}'.format(stream.name.split(sep='/')[-1], paths[0]))
#    shutil.copy2(stream.name, paths[0])
