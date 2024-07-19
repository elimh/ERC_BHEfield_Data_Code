import numpy as np
from dateutil.relativedelta import *
from sklearn.metrics import mean_absolute_error as mae 

def get_vault_outliers_median_filter(data, after = '_T_in', threshold=0.15, return_medians = True, masked_BHEs = None):#kernel_size=[1,7], 
    # finds the BHEs for a certain "data" period whose offset from the median of all BHEs in the vault is higher than "threshold".
    west_in, south_in, east_in = get_ID_strings(after=after, masked_BHEs = masked_BHEs)
    med_west = np.nanmedian(data[west_in].values.T, axis=0)
    med_south = np.nanmedian(data[south_in].values.T, axis=0)
    med_east = np.nanmedian(data[east_in].values.T, axis=0)
    mean_misfit_dict = {}
    for f in west_in:
        mask = np.isnan(data[f])+np.isnan(med_west)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0] == True:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_west[~mask],data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})
    for f in east_in:
        mask = np.isnan(data[f])+np.isnan(med_east)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0] == True:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_east[~mask],data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})
    for f in south_in:
        mask = np.isnan(data[f])+np.isnan(med_south)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0] == True:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_south[~mask],data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})
    if return_medians == True:
        return mean_misfit_dict, {'med_west': med_west, 'med_south': med_south, 'med_east': med_east}
    else:
        return mean_misfit_dict

def generate_ID_strings_per_shaft(before='Probe_', after='_T_in'):
    # replicate from the ERC.plot.Management class
    west_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    south_ids = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25]
    east_ids = [23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

    west = [f'{before}{x:02}{after}' for x in west_ids]
    south = [f'{before}{x:02}{after}' for x in south_ids]
    east = [f'{before}{x:02}{after}' for x in east_ids]
    return west, south, east

def get_ID_strings(after='T_in', masked_BHEs=None):
    west, south, east = generate_ID_strings_per_shaft(after=after)
    if masked_BHEs is not None:
        for masked in masked_BHEs: 
            if masked in west:
                west.remove(masked)
            elif masked in south:
                south.remove(masked)
            elif masked in east:
                east.remove(masked)
    return west, south, east
