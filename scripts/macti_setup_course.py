import os, shutil, pkg_resources

from colorama import Fore, Back, Style

def print_macti_info(msg):
    print(Fore.GREEN + '[MACTI | INFO] ' + Style.RESET_ALL, end = '')
    print(Back.WHITE + ' --> ' + msg + Style.RESET_ALL, end='\n')

def make_dirs(paths):
    for p in paths:
        if not os.path.exists(p):
            print_macti_info('Creando el directorio : {}  '.format(p))
            os.makedirs(p , exist_ok=True)
        else:
            print_macti_info('El directorio : {} ya existe  '.format(p))
    
def copy_files(filenames, abspath, path):
    for f in filenames:
        stream = pkg_resources.resource_stream('macti', os.path.join("resources", f))
        print_macti_info('Copiando {} al directorio {}  '.format(stream.name.split(sep='/')[-1], path))
        shutil.copy2(stream.name, os.path.join(abspath, path))

# ---------------------------
if __name__ == "__main__":

    os.system('clear')
    
    line_len = 50
    print()
    print(Fore.WHITE + Back.GREEN + line_len*'-')
    print(Fore.WHITE + Back.GREEN + '    MACTI: Creación del repositorio del curso     ' + Style.RESET_ALL)
    print(Fore.WHITE + Back.GREEN +  line_len*'-')
    print(Style.RESET_ALL)
    
    c_name = input(' Nombre del curso : ')
    print()

    # --- Creación de directorios ---
    abspath = os.getcwd()
    paths = [c_name,
             os.path.join(c_name, 'Tema1'), 
             os.path.join(c_name, '.ans'), 
             os.path.join(c_name, 'resources'), 
            ]
    make_dirs(paths)

    # --- Iniciar el repositorio local con git ---
    print_macti_info('Cambiando al directorio : {}  '.format('/' + c_name + '/'))
    os.chdir(c_name)
    
    print_macti_info('Iniciando el repositorio  ')
    os.system('git init')
    
    print_macti_info('Cambiando el nombre de la rama principal a main')
    os.system('git branch -M main')

    # --- Crear el archivo .gitignore ---
    lines = ["# NBGRADER \n",
             "nbg/ \n\n",
             "# QUIZ \n",
             "q*.ipynb \n",
             ".ans/ \n",
             ".nbgex \n",
             "# TOOLS \n",
             "resources/ \n",
             "macti_nbg_qs.py \n",
             "assignments_creation.csv \n",
             "assignments_update.csv \n"]
    
    print_macti_info('Creando ' + Style.BRIGHT + '.gitignore ')
    with open(".gitignore", "w") as f:
        f.writelines(lines)

    # --- Copiar archivos ---
    filenames = ['plantilla.ipynb', 
                 'q1_plantilla.ipynb']
    copy_files(filenames, abspath, paths[1])
    
    filenames = ['nbgex', 
                 'assignments_creation.csv', 
                 'assignments_update.csv', 
                 'macti_nbg_qs.py']
    copy_files(filenames, abspath, paths[0])
    os.rename(os.path.join(abspath, paths[0],'nbgex'), 
              os.path.join(abspath, paths[0],'.nbgex'))

    filenames = ['calificador.ipynb',
                 'preproc_gb.ipynb',
                 'test_evaluation.ipynb',
                 'test_visual.ipynb',
                 'interactivo_test.ipynb']
    copy_files(filenames, abspath, paths[3])

    # --- Actualizar el repositorio ---
    print_macti_info('Estado del repositorio  (git status)')
    os.system('git status')
    print_macti_info('Actualizando los cambios (git add .) ')
    os.system('git add .')
    os.system('git status')
    print_macti_info('Confirmando los cambios (git commit -m " ... ")')
    os.system('git commit -m "Iniciando el repositorio"')
    print_macti_info('Estado del repositorio  (git status)')
    os.system('git status')



