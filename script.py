"""
scipt.py - additional function used in the GUI
Copyright 2021: Zechang Sun
Email: sunzc18@mails.tsinghua.edu.cn
"""
import numpy as np
import os
import pandas as pd


def load(files, file_type):
    if file_type == "npz Files (*.npz)":
        return load_npz_files(files)
    else:
        print("Not Support Load %s Files yet..." % file_type)


def save(result, file, file_type):
    if file_type == "CSV File (*.csv)":
        header = ["File", "BAL", "DLA", "Associated DLA", "Interesting", "z", "comment"]
        df = pd.DataFrame(result)
        df[header].to_csv(file, index=False, columns=header)
    else:
        print("Not Support Save %s Files yet..." % file_type)


def load_npz_files(files):
    data = []
    # note: spectra should not be in rest frame
    for file in files:
        spec = np.load(file)
        data.append({"file": file, "wav": spec["wav"], "flux": spec["flux"], "error": spec["err"], "z": float(spec["z"])})
    return data


def save_cont(result, data, dir):
    for idx, (r, d) in enumerate(zip(result, data)):
        name = os.path.split(d["file"])
        np.savez(os.path.join(dir,  name[-1]), name=d["file"], wav=d["wav"]/(1+d["z"]), flux=d["flux"], err=d["error"], z=d["z"], contX=r["cont"][0], contY=r["cont"][1])
