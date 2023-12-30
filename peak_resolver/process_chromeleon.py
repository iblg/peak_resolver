import pandas as pd
import numpy as np
from matplotlib import colormaps
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pathlib
from scipy.interpolate import griddata

def process_file(filepath, tmin=6.5, tmax=9):
    with open(filepath, 'r') as infile:
        lines = infile.read().strip()

    lines = lines.split('\n')
    lines = [line.split('\t') for line in lines]
    lines = lines[44:-1]
    data = pd.DataFrame(lines, columns = ['t', 'step', 's'], dtype='float')
    data = data.drop(columns='step')
    data['ds'] = data['s'].diff()
    data['d2s'] = data['ds'].diff()
    
    data = data.where(data['t'] > tmin).where(data['t'] < tmax).dropna()
    
    return data

def process_chromeleon_file(filepath: pathlib.PosixPath, tmin: float, tmax: float, tgrid:np.array=None):
    '''
    '''
    with filepath.open() as f: 
        lines = f.readlines()
   
    lines = [line.strip().split('\t') for line in lines]
    lines = lines[44:-1]
    data = pd.DataFrame(lines, columns = ['t', 'step', 's'], dtype='float')
    data = data.drop(columns='step')

    if tgrid is None:
        tgrid = np.linspace(tmin, tmax, data.shape[0])
    
    # data['t'] = tgrid

    data2 = pd.DataFrame(tgrid, columns=['t'])
    data2['s'] = griddata(data['t'], data['s'], tgrid)
    data2['ds'] = data2['s'].diff()
    data2['d2s'] = data2['ds'].diff()
    data2 = data2.where(data2['t'] > tmin).where(data2['t'] < tmax).dropna()
    return data2
    
    # data['s'] = griddata(data['t'], data['s'], tgrid)
    # data['ds'] = data['s'].diff()
    # data['d2s'] = data['ds'].diff()
    # data = data.where(data['t'] > tmin).where(data['t'] < tmax).dropna()
    
    # return data

def process_conc_series(prefix, postfix, numbers = None, tmin=6.5, tmax=9):
    if numbers is None:
        numbers = [1,2,3,4,5,6]
    else:
        pass
        
    filepaths = [prefix + str(c) + postfix for c in numbers]

    data = []
    for file in filepaths:
        data.append(process_file(file,tmax=tmax, tmin=tmin))
    
    return data



def plot_cal_series(samples, concentrations, fig=None, ax=None, 
                    plot_type = 'ds', xbounds = (6.6, 9.0), cmap = colormaps['Blues'], 
                    offset = 0, savefig=None):
    norm = colors.Normalize(vmin=min(concentrations), vmax=max(concentrations))
    
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(10,4))
        print('initializing a plot')
    else:
        pass

    
    for sample, c in zip(samples, concentrations):
        ax.plot(sample['t'], sample[plot_type] + offset, color = cmap(norm(c)),label=c)

    if savefig is None:
        pass
    else:
        fig.savefig(savefig, bbox_inches='tight')
        print('saving at {}'.format(savefig))
    return fig, ax

def plot_experiment(fsamps, rsamps, fig=None, ax=None, run=None, desc=None, plot_type='s', savefig=False, t_bounds: tuple = (0,20), legend=True):
    if fig is None and ax is None:
        fig, ax = plt.subplots(nrows=2, figsize=(10,8), sharex=True, sharey=True)
        print('initializing a plot')
    else:
        pass

    ax[0].text(0.05, 0.95, 'Feed', transform = ax[0].transAxes, va = 'top', ha='left')
    ax[1].text(0.05, 0.95, 'Receiver', transform = ax[1].transAxes, va = 'top', ha='left')

    if desc:
        ax[0].text(0.95, 0.95, desc, transform = ax[0].transAxes, va = 'top', ha='right')

    if run:
        ax[0].text(0.95, 0.85, 'Run {}'.format(run), transform = ax[0].transAxes, va = 'top', ha='right')
    
    for i, (fsamp, rsamp) in enumerate(zip(fsamps, rsamps)):
        ax[0].plot(fsamp['t'].where(fsamp['t'] < t_bounds[1]).where(fsamp['t'] > t_bounds[0]), fsamp[plot_type], label = i)
        ax[1].plot(rsamp['t'].where(fsamp['t'] < t_bounds[1]).where(fsamp['t'] > t_bounds[0]), rsamp[plot_type])


    ax[0].set_xlim(t_bounds)

    if legend:
        ax[0].legend(loc='lower right', ncol=3, title = 'Time [h]')
    

    if savefig is False:
        pass
    else:
        fig.savefig(savefig, bbox_inches='tight')

    return fig, ax



        
