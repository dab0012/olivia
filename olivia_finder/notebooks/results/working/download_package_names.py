'''
    Script to download the list of packages from the NPM repository
'''
import sys
import os
from typing import List, Optional
from tqdm import tqdm

# Add the path to the olivia_finder package
sys.path.append('/home/dnllns/Documentos/repositorios/olivia-finder/olivia_finder/')
from olivia_finder.myrequests.request_handler import RequestHandler


# Auxiliary function to download a page of documents from the NPM repository

def download_page(
    start_key: Optional[str]=None, 
    size: Optional[int]=1000, 
    retries: Optional[int]=5,
    rh: RequestHandler = RequestHandler()
)-> List[dict]:

    NPM_PACKAGE_LIST_URL = 'https://skimdb.npmjs.com/registry/_all_docs'

    # Fix for the first page
    if start_key is None:
        params = {'limit': size}
    else:
        encode_start_key = "\"" + start_key + "\""
        params = {'startkey': encode_start_key, 'limit': size}

    r = rh.do_request(NPM_PACKAGE_LIST_URL, params=params)[1]
    
    # If the response is None, return an empty list
    if r is None:
        print(f'None response at download_page: url={NPM_PACKAGE_LIST_URL}')
        return []
                    
    # If the response returns an error, return an empty list
    try:
        data = r.json()

    except Exception as x:
        print(f'EXCEPTION at __download_page: url={NPM_PACKAGE_LIST_URL}')
        print(f'Error parsing JSON: {x}')
        print(f'Response: {r.text}')
        print(f'Params: {params}')
        print(f'Retrying, times left: {retries}')
        return download_page(rh, start_key, size, retries-1)

    # If the response returns an error, make a new request recursively until the retries are over
    if data.keys() == {'error', 'reason'}:
        return download_page(rh, start_key, size, retries-1)
    else:
        # Return the list of packages
        # Fix of selecting by last key
        return data['rows'][1:]


def donwload_package_names(last_key: Optional[str]=None, next_page_=0, total_pages_=0) -> List[str]:

    # # Cargar los paquetes ya obtenidos en una lista
    # package_names = []
    # with open(f'{WORKING_FOLDER}/nombre_paquetes.txt', 'r', encoding='utf-8') as f:
    #     package_names.extend(line.strip() for line in f)

    # Initialize the progress bar if is set
    progress_bar = tqdm(total=total_pages_)

    # Obtain the names of the packages requesting the pages
    pages = []
    for i in range(total_pages_):

        current_page_ = i + next_page_

        page_ = download_page(last_key, PAGE_SIZE)

        # check if the page is empty
        if len(page_) == 0:
            print(f'Empty page {current_page_} of {total_pages_}')
            print(f'Last key: {last_key}')
            continue

        pages.append(page_)

        # get the last key of the page for the next iter
        last_key = page_[-1]['id']

        # Save chunk if is set
        with open(f'{CHUNKS_FOLDER}/chunk_{current_page_}.json', 'w', encoding='utf-8') as f_:
            f_.write(str(page_))            

        # Update progress bar if is set
        progress_bar.update(1)
        progress_bar.set_description(f'Page {current_page_} of {total_pages_}, last key: {last_key}')

    progress_bar.close()


## ------------------ MAIN ------------------ ##
# -------------------------------------------- #

NPM_PACKAGE_REGISTRY_URL = 'https://skimdb.npmjs.com/registry'
'''endpoint to get the total number of packages'''

PAGE_SIZE = 100
'''Number of packages to be downloaded per page'''

WORKING_FOLDER = os.path.dirname(__file__)
'''Folder where the script is located'''

CHUNKS_FOLDER = os.path.join(WORKING_FOLDER, 'npm')
'''Folder where the chunks of packages will be stored'''

RH = RequestHandler()
'''Request handler to make the requests'''


if __name__ == '__main__':

    completed = False
    exception_count = 0

    while not completed:
        try:

            package_names = []
            # recorre cada archivo .json de este directorio y extrae los nombres de los paquetes
            data_path = os.listdir(CHUNKS_FOLDER)
            continue_processing = True
            current_page = 0

            while continue_processing:

                file_name = f'chunk_{current_page}.json'
                if file_name in data_path:
                    curr_file = f'{CHUNKS_FOLDER}{os.sep}{file_name}'
                    with open(curr_file, 'r', encoding='utf-8') as f:
                        page = eval(f.read())

                    package_names.extend(diccionario['key'] for diccionario in page)
                    print(f'Page {current_page} processed')
                    current_page += 1

                else:
                    print('No more files to process')
                    continue_processing = False

            # # guardar los nombres de los paquetes en un archivo de texto
            # with open(f'{WORKING_FOLDER}/nombre_paquetes.txt', 'w', encoding='utf-8') as f:
            #     for nombre in nombre_paquetes:
            #         f.write(nombre + '\n')

            # Get the number of the next page to be downloaded
            next_page = sum(
                1 for file in os.listdir(CHUNKS_FOLDER) if file.endswith('.json')
            )

            # Get the total number of packages
            # Tener en cuenta los paquetes ya obtenidos
            response = RH.do_request(NPM_PACKAGE_REGISTRY_URL)[1]
            total_packages = response.json()['doc_count']
            total_packages -= len(package_names)

            # Calculate the number of pages (chunks)
            total_pages = (total_packages // PAGE_SIZE) + 1

            donwload_package_names(
                last_key=package_names[-1], 
                next_page_=next_page, 
                total_pages_=total_pages
            )
            completed = True


        except Exception as e:
            exception_count += 1
            print(f'EXCEPTION at __main__: {e}')
            print(f'Exception count: {exception_count}')
