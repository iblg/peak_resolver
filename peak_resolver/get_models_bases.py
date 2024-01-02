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
    # print('\n\n\n Calibration dataset:')
    # print(data)

    basis_funcs = []
    for coord in coords_list:
        # print(coord)
        unwanted = list(coords_list)
        # print(unwanted)
        unwanted.remove(coord)
        # print(unwanted)
        # x = data.drop_dims(unwanted)
    

        x = data.sel({coord:conc})
        for acid in unwanted:
            x = x.sel({acid:0})
        x = x.dropna(dim='t', how='all')[order]
        print('\n\n\n {} dataset:'.format(coord))
        # print(x)

        basis_funcs.append(x)

    


    return basis_funcs