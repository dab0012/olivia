import math
import pandas as pd
import tqdm as tqdm
import gc as gc

# Add the project root to the python path so that we can import modules
import sys
sys.path.append("/home/dnllns/Documentos/repositorios/olivia-finder/olivia_finder")

# Set environment variable for the config file
import os
os.environ['OLIVIA_FINDER_CONFIG_FILE_PATH'] = "/home/dnllns/Documentos/repositorios/olivia-finder/olivia_finder/config.ini"


from olivia_finder.data_source.repository_scrapers.npm import NpmScraper
from olivia_finder.myrequests.request_handler import RequestHandler

packages_file = "/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/package_lists/npm_packages_full_list.txt"
out_folder = "/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/csv_datasets/npm/chunks"

# Leer fichero de paquetes
# ------------------------
f1 = open(packages_file, "r")
packages = f1.readlines()
print(f"Total number of packages: {len(packages)}")

# Separacion en lotes 
# -------------------
batch_size = 10000

num_batches = math.ceil(len(packages) / batch_size)
print(f"Number of batches: {num_batches}")
batched_packages = []
for i in range(num_batches):
    batch = packages[i*batch_size:(i+1)*batch_size]

    # Remove new line characters
    batch = [package.replace("\n", "") for package in batch]
    batched_packages.append(batch)

# Liberamos memoria
del packages
gc.collect()

# Set up de la carpeta de salida y el fichero de paquetes no encontrados
# ---------------------------------------------------------------------

# Create the output folder if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# Set up the not found packages file
not_found_file = open(f"{out_folder}/npm_packages_not_found.txt", "w")
not_found_file.close()

# Scraping de los paquetes
# ------------------------
print("Scraping packages...")
scraper = NpmScraper()

# Iteramos sobre los lotes de paquetes
for batch in tqdm.tqdm(batched_packages):

    batch_id = batched_packages.index(batch)
    found, not_found = scraper.obtain_packages_data(batch)
    print(f"Found: {len(found)}")
    print(f"Not found: {len(not_found)}")

    # Guardamos los paquetes no encontrados en un fichero
    with open(f"{out_folder}/npm_packages_not_found.txt", "a") as f:
        for package in not_found:
            f.write(f"{package}\n")

    # liberamos memoria
    del not_found
    gc.collect()

    # Exportamos los paquetes encontrados a un csv
    df = pd.DataFrame()

    batch_data = []
    for package in found:
        if package["dependencies"] is None:
            batch_data.append({
                'name': package["name"],
                'version': package["version"],
                'dependency': None,
                'dependency_version': None,
            })
        else:
            for dependency in package["dependencies"]:
                batch_data.append({
                    'name': package["name"],
                    'version': package["version"],
                    'dependency': dependency["name"],
                    'dependency_version': dependency["version"],
                })
    
    # Clear memory
    del found
    gc.collect()

    # Convertimos la lista de diccionarios en un dataframe y lo guardamos en un csv
    df = pd.DataFrame(batch_data)
    df.to_csv(f"{out_folder}/npm_packages_found_{batch_id}.csv", index=False)

    # Clear memory
    print("Clearing memory...")
    del df
    del batch_data
    gc.collect()

print("Scraping done!")

# Juntamos los csvs en uno solo
# -----------------------------

print("Concatenating csvs...")
dfs = []
for i in tqdm.tqdm(range(num_batches)):
    df = pd.read_csv(f"{out_folder}/npm_packages_found_{i}.csv")
    dfs.append(df)

    # Clear memory
    del df
    gc.collect()


df = pd.concat(dfs)
df.to_csv(f"{out_folder}/all_npm_packages_found.csv", index=False)
print("All done!")

