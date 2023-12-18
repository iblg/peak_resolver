import pandas as pd
import xarray as xr
from process_chromeleon.process_chromeleon import *
import os
import re
import numpy as np

def flatten(matrix):
    return [item for row in matrix for item in row]

def get_cal_curve_dataset(data_list, fpath_list):
    data_list = flatten(data_list)
    fpath_list = flatten(fpath_list)
    conc = {'1':0.05, '2':0.1, '3':0.2, '4':0.3, '5':0.4, '6':0.4}
    chems = ['A', 'P', 'B', 'V', 'C']

    for data, name in zip(data_list, fpath_list):
        for c in chems:
            data[c] = 0
        
        data[name[0]] = float(conc[name[1]])
    
    
    df = data_list[0]
    for i in data_list[1:]:
        df = pd.concat([df, i])

    indices = chems
    indices.append('t')
    df = df.set_index(indices)
    df = df.sort_values(['A', 'P', 'B', 'V', 'C'])

    # for i in df.iterrows():
    #     print(i)
    # # data_list = [data.set_index(indices) for data in data_list]
    # data_list = [d.to_xarray() for d in data_list]
    idx = df.index()
    df = df.drop
    ds = df.to_xarray()
    return ds

def read_cal_curve_to_list(top_path):
    os.chdir(top_path)
    cwd = os.getcwd()
    exp_dirs = os.listdir()[1:]

    data_list, fpath_list = [], []
    for exp_dir in exp_dirs:
        os.chdir(os.path.join(top_path, exp_dir))
        file_paths = [f for f in os.listdir() if '.txt' in f]
        files = [process_file(f) for f in os.listdir() if '.txt' in f]
        fpath_list.append(file_paths)
        data_list.append(files)
    return data_list, fpath_list

def read_dataset_to_list(top_path):
    tgrid = np.linspace(0.15, 19.85, 5997)

    os.chdir(top_path)
    cwd = os.getcwd()
    exptl_dirs = os.listdir()[1:]
    data_list = []
    for dir in exptl_dirs:
        run_dirs = os.listdir(cwd + '/' + dir)
        run_dirs = list(filter(lambda x: 'RUN' in x, run_dirs))
        for run_dir in run_dirs:
            files = os.listdir(cwd + '/' + dir + '/' + run_dir)
            files = list(filter(lambda x: '.txt' in x, files))

            first = 0
            for file in files:
                filename = cwd + '/' + dir + '/' + run_dir + '/' + file
                data = process_file(filename, tmin=0, tmax=20)
                data = interpolate_time(data, tgrid)
                data['side'] = file[0]
                data['exp_time'] = float(file[1])

                run_idx = (re.search('_', file)).start() - 1
                data['run'] = int(file[run_idx])
                chems = ['Acetic', 'Propionic', 'Butyric', 'Valeric', 'Caproic']
                comp = get_comp(file, chems)

                for chem in chems:
                    data[chem] = comp[chem].iloc[0]
                data = data.drop(columns=['s', 'ds', 'd2s'])
                data = data.rename(columns={'s_interp': 's', 'ds_interp': 'ds', 'd2s_interp': 'd2s'})
                data['tgrid'] = tgrid
                data_list.append(data)
    return data_list

def read_list_to_ds(data):
    df = data[0]

    for i in data[1:]:
        df = pd.concat([df, i])
    df = df.reset_index()
    return df


def get_comp(file, chems):
    dash = re.search('-', file).start()
    und = re.search('_', file).start()
    range = (dash, und)
    slice = file[dash + 1: und]

    keys = ['A', 'P', 'B', 'V', 'C']

    comp = pd.DataFrame([[0, 0, 0, 0, 0]], columns=chems)
    for k, chem in zip(keys, chems):
        if k in slice:
            comp[chem] = 50
        else:
            comp[chem] = 0
    return comp


from scipy.interpolate import griddata
from scipy.signal import resample


def interpolate_time(data, tgrid):
    for i in ['s', 'ds', 'd2s']:
        data[i + '_interp'] = griddata(np.array(data['t']), np.array(data[i]), tgrid)
    return data


def resample_time(data, npoints=5997):
    for i in ['s', 'ds', 'd2s']:
        data[i] = resample(data[i], npoints)
    return data
