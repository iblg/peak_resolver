from pathlib import Path
import pickle
import xarray as xr

def get_models(root_dir:str, acids:list):
    mods = {}
    p = Path(root_dir).resolve()
    for acid in acids:
        print(acid)
        q = p / (acid.upper() + ' ACID')
        q = q / 'model' / 'model.pkl'
        with open(q, 'rb') as infile:
            mod = pickle.load(infile)
        mods[acid[:3]] = mod
    
    return mods
    
def get_basis_functions(fp:str, 
                        conc:float = 0.5, 
                        coords_list: tuple = ('Acetic', 'Propanoic', 'Butyric', 'Valeric', 'Caproic'),
                        order = 'ds'
                       ):
    data = xr.load_dataset(fp)

    basis_funcs = []
    for coord in coords_list:
        x = data.sel({coord:conc}).dropna(dim='t', how='all')[order]
        basis_funcs.append(x)

    


    return basis_funcs