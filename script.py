import numpy as np
import csv


def load(files, file_type):
    if file_type == "npz Files (*.npz)":
        return load_npz_files(files)
    else:
        print("Not Support Load %s Files yet..." % file_type)


def save(result, file, file_type):
    if file_type == "CSV File (*.csv)":
        with open(file, "w", newline="") as csvfile:
            header = ["File", "BAL", "DLA", "Associated DLA", "Interesting", "z", "comment"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(result)
    else:
        print("Not Support Save %s Files yet..." % file_type)


def load_npz_files(files):
    data = []
    for file in files:
        spec = np.load(file)
        data.append({"file": file, "wav": spec["wav"], "flux": spec["flux"], "error": spec["err"], "z": float(spec["z"])})
    return data

