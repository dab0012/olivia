import tqdm as tqdm

# Leer ficheros
f1 = open("/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/package_lists/npm_librariesio.txt", "r")
p1 = f1.readlines()
print(len(p1))
f2 = open("/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/package_lists/npm_registry.txt", "r")
p2 = f2.readlines()
print(len(p2))

# Concatenar ficheros sin duplicados
packages = list(set(p1 + p2))
print(f"Total number of packages: {len(packages)}")

# Ordenar paquetes alfabeticamente
packages.sort()

# Guardamos los paquetes en un fichero
with open("/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/package_lists/npm_packages_full_list.txt", "w") as f:
    for package in tqdm.tqdm(packages):
        f.write(package)

print('Done!')

