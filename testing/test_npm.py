# import requests

# # URL para obtener los datos del paquete
# url = 'https://replicate.npmjs.com/@0y0%2fgitbook-cli'

# # Hacer una solicitud GET a la URL
# response = requests.get(url)

# # Obtener los datos en formato JSON
# data = response.json()

# # Obtener el nombre del paquete
# package_name = data['name']

# # Obtener la URL del paquete
# package_url = f'https://www.npmjs.com/package/{package_name}'

# # Obtener las dependencias de la última versión disponible
# dependencies = data['versions'][data['dist-tags']['latest']]['dependencies']

# print(f'Nombre del paquete: {package_name}')
# print(f'URL del paquete: {package_url}')
# print(f'Dependencias de la última versión: {dependencies}')



# import requests
# from concurrent.futures import ThreadPoolExecutor
# from functools import partial

# from tqdm import tqdm

# # URL para obtener el numero total de paquetes en el registro (Json field: 'doc_count')
# url_registry = 'https://skimdb.npmjs.com/registry'

# # URL para obtener los datos de los paquetes
# url = 'https://skimdb.npmjs.com/registry/_all_docs'

# # Get the total number of packages
# response = requests.get(url_registry)
# total_packages = response.json()['doc_count']

# # Tamaño de página
# page_size = 2000

# # Función para descargar una página de documentos
# def download_page(start_key, progress_bar):
#     params = {'limit': page_size, 'start_key': start_key}
#     try:
#         response = requests.get(url, params=params)
#     except Exception as e:
#         print(e)
#         # Si hay un error reintente la solicitud 5 veces mas
#         for i in range(5):
#             try:
#                 response = requests.get(url, params=params)
#                 break
#             except Exception as e:
#                 print(e)
#                 continue
            
#             print('No se pudo descargar la página con start_key:', start_key)
    
#     progress_bar.update(1)
#     return response.json()['rows']

# # Obtener la lista de claves de inicio
# start_keys = []
# for i in range(0, total_packages, page_size):
#     start_keys.append(f'"{i}"')

# # show progress of download chunks
# progress_bar = tqdm(total=len(start_keys))
# # Añadir mensaje a la barra de progreso
# progress_bar.set_description('Descargando paquetes')

# func = partial(download_page, progress_bar=progress_bar)

# with ThreadPoolExecutor(max_workers=32) as executor:
#     pages = list(executor.map(func, start_keys))

# # Obtener la lista completa de nombres de paquetes
# package_names = []
# for page in pages:
#     for row in page:
#         if row['id'].startswith('_'):
#             continue
#         package_names.append(row['id'])

# # Imprimir la lista completa de nombres de paquetes
# print("Lista de nombres de paquetes:")
# print(package_names)

# # Almacenaremos los nombres de los paquetes en un archivo de texto csv
# with open('package_names.csv', 'w') as f:
#     f.write('package_name')


import os
import pickle

# Add the olivea_finder directory to the path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from olivia_finder.repo import Repo
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.npm import NpmScraper
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler
from olivia_finder.scrape.requests.proxy_builder import GeonodeProxy

npm = Repo('NPM', 'https://www.npmjs.com/package/')
# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh)

# Initialize cran scraper
ns = NpmScraper(rh)

# Get the list of packages
packages = ns.obtain_package_names()

# Save the list of packages
print('Saving package names...')
with open('./package_names.pkl', 'wb') as f:
    pickle.dump(packages, f)
print('Done!')

# write the package names to a csv file
print('Writing package names to csv file...')
with open('./package_names.csv', 'w') as f:
    f.write('package_name\n')
    for package in packages:
        f.write(package + '\n')
print('Done!')

# Save the list of packages as a text file
print('Writing package names to text file...')
with open('./package_names.txt', 'w') as f:
    for package in packages:
        f.write(package + '\n')
print('Done!')