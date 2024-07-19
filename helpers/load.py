import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import *

def load_raw_data(start_date, end_date, BHEs=None, masked=False):
    ## load the raw data for a given time period and selected BHEs (list, ndarray, str or int)
    if BHEs == None:
        BHEs = np.arange(1,41,1)
    else:
        if not isinstance(BHEs, list) or isinstance(BHEs, np.ndarray):
            BHEs = [BHEs]
    if not isinstance(BHEs[0], str):
        BHEs = [f'{x:02d}' for x in BHEs]
        column_select = []
        for BHE in BHEs:
            column_select.append(f'Probe_{BHE}_T_in')
            column_select.append(f'Probe_{BHE}_T_out')
            column_select.append(f'Probe_{BHE}_V_dot')

    BHE_data =pd.DataFrame() 
    time_format = "%Y-%m-%d %H:%M:%S"
    time_start_global = dt.strptime(start_date,time_format)
    time_end_global=dt.strptime(end_date,time_format)
    timeStep = relativedelta(months=+1)  
    time_start=time_start_global

    while time_start <= time_end_global:
        loadname=f"data/raw_30s/ERC_data_raw_{time_start.year}_{time_start.month:02d}.csv"
        data = pd.read_csv(loadname)
        data.index = pd.to_datetime(data['Time'], utc=True)
        data.index = data.index.tz_localize(None)
        if len(BHEs)==40:
            BHE_data = pd.concat((BHE_data, data))  
        else:
            BHE_data = pd.concat((BHE_data, data[column_select])) 
        time_start+=timeStep
    BHE_data= BHE_data.loc[time_start_global:time_end_global]
    if masked == True:
        for BHE in BHEs:
            mask = create_BHE_data_mask(BHE_data, BHE)
            BHE_data.loc[mask, [f'Probe_{BHE}_T_in', f'Probe_{BHE}_T_out', f'Probe_{BHE}_V_dot']] = np.nan 
    return BHE_data


def create_BHE_data_mask(data, BHE, timestep=30):
    # uses T_in, T_out and V_dot and creates a mask with the same shape
    # masks noflow, if one timeseries has a datagap, and the next n steps after it, depending on the horizontal pipe length
    if isinstance(BHE, int):
        BHE = f'{BHE:02d}'

    # Number of steps to mask after encountering a NaN or zero (depending on total pipe length)
    time_to_mask = masking_times.get(BHE)
    nsteps = int(-(-time_to_mask // timestep)) # rounds up to the next integer
    min_gap_size = 20

    # Initialize the boolean mask
    mask = np.zeros_like(data[f'Probe_{BHE}_T_in'].values, dtype=bool)

    # Create zero volflow mask
    mask_volflow = data[f'Probe_{BHE}_V_dot'].values < 0.5

    #### Create a boolean mask for no data volflow
    mask_nan_volflow = np.zeros_like(data[f'Probe_{BHE}_V_dot'].values, dtype=bool)

    # Find the start and end of NaN sequences
    nan_diff = np.diff(np.concatenate(([0], np.isnan(data[f'Probe_{BHE}_V_dot'].values), [0])))
    nan_starts = np.where(nan_diff == 1)[0]
    nan_ends = np.where(nan_diff == -1)[0]

    # Apply the condition for NaN sequences longer than min_gap_size, plus the next nsteps positions
    for start, end in zip(nan_starts, nan_ends):
        if end - start > min_gap_size:
            mask_nan_volflow[start:min(end + nsteps, len(data[f'Probe_{BHE}_V_dot'].values))] = True
    ### End creation boolean mask nodata volflow

    # Combine both conditions
    combined_mask = mask_nan_volflow | mask_volflow
    # Find indices where combined_mask is True
    indices = np.where(combined_mask)[0]
    # Set mask to True for these indices and the next nsteps
    for idx in indices:
        mask[idx:idx + nsteps + 1] = True
    # Ensure the mask does not go out of bounds
    return mask[:len(data[f'Probe_{BHE}_T_in'].values)]

# time to mask after a noflow or datagap period (depending on pipelength) - calculated in calculate_fluid_travel_time.ipynb
masking_times = {'01': 625.36,
 '02': 593.24,
 '03': 585.96,
 '04': 626.64,
 '05': 668.18,
 '06': 706.72,
 '07': 745.26,
 '08': 567.54,
 '09': 593.24,
 '10': 640.34,
 '11': 672.46,
 '12': 638.2,
 '13': 807.36,
 '14': 723.85,
 '15': 683.17,
 '16': 642.48,
 '17': 601.8,
 '18': 563.26,
 '19': 563.26,
 '20': 603.94,
 '21': 642.48,
 '22': 685.31,
 '23': 693.87,
 '24': 721.71,
 '25': 651.05,
 '26': 616.79,
 '27': 651.05,
 '28': 597.52,
 '29': 631.78,
 '30': 578.25,
 '31': 618.93,
 '32': 563.26,
 '33': 573.97,
 '34': 614.65,
 '35': 629.64,
 '36': 655.33,
 '37': 614.65,
 '38': 648.91,
 '39': 708.86,
 '40': 747.4}
