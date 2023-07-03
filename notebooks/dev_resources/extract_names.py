# Abre los archivos de texto y extrae los nombres de los paquetes
# cada archivo esta estructurado en forma de lista de diccionarios:
# [
#     {'id': 'essupernext', 'key': 'essupernext', 'value': {'rev': '5-1d3f17e286afc66522130cc6dcfc1707'}},
#     {'id': 'essurvey', 'key': 'essurvey', 'value': {'rev': '5-6a8a4d7d0104bb5c5150b9007c7d85e4'}},
#     {'id': 'essy-code-parser', 'key': 'essy-code-parser', 'value': {'rev': '17-175feec3709650ab47c12ef9fe707200'}},

# ]
# almacenara el valor de la llave 'key' en una lista

import os
nombre_paquetes = []

# Geth this file's parent folder
working_folder = os.path.dirname(os.path.abspath(__file__))
print("wwwwwwwwwww", working_folder)


# recorre cada archivo .json de este directorio y extrae los nombres de los paquetes
data_path = os.listdir(f"{working_folder}/npm")
continue_processing = True
current_page = 0

while continue_processing:

    file_name = f"chunk_{current_page}.json"
    if file_name in data_path:
        curr_file = f"{working_folder}/npm/{file_name}"
        with open(curr_file, 'r', encoding='utf-8') as f:
            page = eval(f.read())

        nombre_paquetes.extend(diccionario['key'] for diccionario in page)
        print(f'Page {current_page} processed')
        current_page += 1

    else:
        continue_processing = False

# guardar los nombres de los paquetes en un archivo de texto
with open(f"{working_folder}/nombre_paquetes.txt", 'w', encoding='utf-8') as f:
    for nombre in nombre_paquetes:
        f.write(nombre + '\n')

