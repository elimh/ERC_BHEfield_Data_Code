import numpy as np
from dateutil.relativedelta import *
from sklearn.metrics import mean_absolute_error as mae 
    
def get_vault_outliers_median_filter(data, after='_T_in', threshold=0.15, return_medians=True, masked_BHEs=None):
    """
    Identifies the Borehole Heat Exchangers (BHEs) whose offset from the median of all BHEs 
    in the vault exceeds a specified threshold.

    Parameters:
    data (pd.DataFrame): DataFrame containing the BHE data.
    after (str): Suffix to filter BHE IDs. Default is '_T_in'.
    threshold (float): Threshold value to identify outliers based on mean absolute error. Default is 0.15.
    return_medians (bool): If True, returns the medians of BHE groups along with the outliers. Default is True.
    masked_BHEs (list or None): List of BHE IDs to be excluded from the analysis. Default is None.

    Returns:
    dict: A dictionary with BHE IDs as keys and their mean misfit values as values.
    dict (optional): If return_medians is True, returns a second dictionary with the medians of the BHE groups.
    """

    # Get the BHE ID strings for west, south, and east groups
    west_in, south_in, east_in = get_ID_strings(after=after, masked_BHEs=masked_BHEs)

    # Calculate the median for each BHE group
    med_west = np.nanmedian(data[west_in].values.T, axis=0)
    med_south = np.nanmedian(data[south_in].values.T, axis=0)
    med_east = np.nanmedian(data[east_in].values.T, axis=0)

    mean_misfit_dict = {}

    # Calculate mean misfit for the west group and identify outliers
    for f in west_in:
        mask = np.isnan(data[f]) + np.isnan(med_west)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0]:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_west[~mask], data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})

    # Calculate mean misfit for the east group and identify outliers
    for f in east_in:
        mask = np.isnan(data[f]) + np.isnan(med_east)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0]:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_east[~mask], data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})

    # Calculate mean misfit for the south group and identify outliers
    for f in south_in:
        mask = np.isnan(data[f]) + np.isnan(med_south)
        if len(np.unique(mask)) == 1 and np.unique(mask)[0]:
            mean_misfit = np.nan
        else:
            mean_misfit = mae(med_south[~mask], data[f][~mask])
        if np.abs(mean_misfit) > threshold:
            mean_misfit_dict.update({f: mean_misfit})

    # Return the mean misfit dictionary and optionally the medians of the groups
    if return_medians:
        return mean_misfit_dict, {'med_west': med_west, 'med_south': med_south, 'med_east': med_east}
    else:
        return mean_misfit_dict

def generate_ID_strings_per_shaft(before='Probe_', after='_T_in'):
    """
    Generate lists of formatted ID strings for different shaft orientations.

    This function generates three lists of formatted ID strings based on predefined 
    identifiers for west, south, and east shafts. The identifiers are combined with 
    the provided prefixes and suffixes to create the final ID strings.

    Args:
        before (str): The prefix string to add before the ID number. Default is 'Probe_'.
        after (str): The suffix string to add after the ID number. Default is '_T_in'.

    Returns:
        tuple: A tuple containing three lists of formatted ID strings:
            - west (list of str): Formatted ID strings for the west shaft.
            - south (list of str): Formatted ID strings for the south shaft.
            - east (list of str): Formatted ID strings for the east shaft.
    """
    
    # Define the identifier lists for each shaft orientation
    west_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    south_ids = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25]
    east_ids = [23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

    # Generate the formatted ID strings for each shaft orientation
    west = [f'{before}{x:02}{after}' for x in west_ids]
    south = [f'{before}{x:02}{after}' for x in south_ids]
    east = [f'{before}{x:02}{after}' for x in east_ids]

    return west, south, east

def get_ID_strings(after='T_in', masked_BHEs=None):
    """
    Generate ID strings for three shafts (west, south, east) and remove any masked BHEs if provided.

    This function calls `generate_ID_strings_per_shaft` to obtain initial ID strings for the
    west, south, and east shafts. If a list of masked BHEs is provided, the function will remove
    these masked BHEs from the corresponding shaft lists.

    Parameters:
    after (str): A string parameter passed to `generate_ID_strings_per_shaft`. Default is 'T_in'.
    masked_BHEs (list): A list of BHEs (Borehole Heat Exchangers) to be masked. Default is None.

    Returns:
    tuple: Three lists containing the ID strings for the west, south, and east shafts respectively.
    """

    # Generate ID strings for each shaft
    west, south, east = generate_ID_strings_per_shaft(after=after)

    # Check if masked_BHEs is provided
    if masked_BHEs is not None:
        for masked in masked_BHEs:
            # Remove masked BHEs from the west list if present
            if masked in west:
                west.remove(masked)
            # Remove masked BHEs from the south list if present
            elif masked in south:
                south.remove(masked)
            # Remove masked BHEs from the east list if present
            elif masked in east:
                east.remove(masked)

    return west, south, east