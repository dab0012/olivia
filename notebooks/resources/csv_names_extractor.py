# Read a csv
# ----------
import pandas as pd
import tqdm as tqdm

df = pd.read_csv("/home/dnllns/Documentos/repositorios/olivia-finder/notebooks/results/csv_datasets/npm/npm_adjlist_librariesio_filtered.csv")
print(df.head())

names_set = set(df["Project Name"])
print(len(names_set))

dependency_set = set(df["Dependency Name"])
print(len(dependency_set))


# Concatenate two sets
# --------------------

full_set = names_set.union(dependency_set)
print(len(full_set))

# Cast full set to a list of strings
full_set = [str(element) for element in full_set]

# Save a set to a txt file
out_path = "notebooks/results/package_lists"
out_file = "npm_librariesio.txt"

with open(f"{out_path}/{out_file}", "w") as f:
    for element in tqdm.tqdm(full_set):
        f.write(element)
        f.write("\n")

