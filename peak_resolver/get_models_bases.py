from pathlib import Path
import pickle

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