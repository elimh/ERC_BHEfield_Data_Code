import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import List, Union, Optional


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
RAW_DATA_DIR = Path("data/raw_30s")
PREPARED_DATA_DIR = Path("data/prepared_5min")


def load_data(
    start_date: str,
    end_date: str,
    BHEs: Optional[Union[List[Union[str, int]], np.ndarray, str, int]] = None,
    masked: bool = False,
    data_type: str = 'raw'
) -> pd.DataFrame:
    """
    Load data for a given time period and selected Borehole Heat Exchangers (BHEs).

    Parameters:
    start_date (str): The start date in the format 'YYYY-MM-DD HH:MM:SS'.
    end_date (str): The end date in the format 'YYYY-MM-DD HH:MM:SS'.
    BHEs (list, ndarray, str, or int, optional): List of BHEs to load. Default is None, 
                                                 which loads all BHEs (1 to 40).
    masked (bool, optional): Whether to mask the data using the create_BHE_data_mask function. 
                             Default is False.
    data_type (str, optional): Type of data to load ('raw' or 'prepared'). Default is 'raw'.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data for the specified BHEs and time period.
    """
    # Set default BHEs if none are provided
    if BHEs is None:
        BHEs = np.arange(1, 41, 1)
    else:
        # Ensure BHEs is a list, convert if necessary
        if not isinstance(BHEs, (list, np.ndarray)):
            BHEs = [BHEs]
    
    # Convert BHEs to string format with leading zeros
    if not isinstance(BHEs[0], str):
        BHEs = [f'{x:02d}' for x in BHEs]
    
    # Prepare list of columns to select
    column_select = []
    for BHE in BHEs:
        column_select.append(f'Probe_{BHE}_T_in')
        column_select.append(f'Probe_{BHE}_T_out')
        column_select.append(f'Probe_{BHE}_V_dot')

    # Initialize empty DataFrame to store BHE data
    BHE_data = pd.DataFrame() 
    
    # Parse start and end dates
    time_start_global = dt.strptime(start_date, TIME_FORMAT)
    time_end_global = dt.strptime(end_date, TIME_FORMAT)
    time_step = relativedelta(months=+1)  
    time_start = time_start_global

    data_dir = PREPARED_DATA_DIR if data_type == 'prepared' else RAW_DATA_DIR

    # Load data month by month within the specified date range
    while time_start <= time_end_global:
        #loadname = f"data/raw_30s/ERC_data_raw_{time_start.year}_{time_start.month:02d}.csv"
        file_path = data_dir / f"ERC_data_{data_type}_{time_start.year}_{time_start.month:02d}.csv"
        data = pd.read_csv(file_path)
        data.index = pd.to_datetime(data['Time'], utc=True)
        data.index = data.index.tz_localize(None)
        
        # Concatenate data for all BHEs or selected columns
        if len(BHEs) == 40:
            BHE_data = pd.concat((BHE_data, data))  
        else:
            BHE_data = pd.concat((BHE_data, data[column_select])) 
        
        # Move to the next month
        time_start += time_step

    # Filter data for the specified date range
    BHE_data = BHE_data.loc[time_start_global:time_end_global]

    # Apply masking if required
    if data_type == 'raw' and masked:
        for BHE in BHEs:
            mask = create_BHE_data_mask(BHE_data, BHE)
            BHE_data.loc[mask, [f'Probe_{BHE}_T_in', f'Probe_{BHE}_T_out', f'Probe_{BHE}_V_dot']] = np.nan 
    
    return BHE_data


def create_BHE_data_mask(data: pd.DataFrame, BHE: Union[int, str], timestep: int = 30) -> np.ndarray:
    """
    Create a boolean mask for Borehole Heat Exchanger (BHE) data based on temperature and flow rate time series.

    This function generates a mask for the provided BHE data to indicate periods of no flow or data gaps.
    The mask is created based on the `T_in`, `T_out`, and `V_dot` columns in the `data` DataFrame. The mask 
    will be True for periods where there is no flow (flow rate below a threshold), or where there are data 
    gaps in the flow rate time series, including a specified number of steps after such gaps, depending on 
    the horizontal pipe length.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the BHE data.
    - BHE (Union[int, str]): The identifier for the Borehole Heat Exchanger. Can be an integer or a string.
    - timestep (int, optional): The timestep in minutes. Default is 30.

    Returns:
    - np.ndarray: A boolean array mask with the same length as the input data series for the BHE.
    """

    # Convert BHE identifier to a zero-padded string if it is an integer
    if isinstance(BHE, int):
        BHE = f'{BHE:02d}'

    # Number of steps to mask after encountering a NaN or zero flow rate
    time_to_mask = MASKING_TIMES.get(BHE)
    nsteps = int(-(-time_to_mask // timestep))  # Round up to the next integer
    min_gap_size = 20

    # Initialize the boolean mask with the same shape as the temperature input series
    mask = np.zeros_like(data[f'Probe_{BHE}_T_in'].values, dtype=bool)

    # Create a mask for zero flow rate
    mask_volflow = data[f'Probe_{BHE}_V_dot'].values < 0.5

    # Create a mask for NaN (no data) in flow rate
    mask_nan_volflow = np.zeros_like(data[f'Probe_{BHE}_V_dot'].values, dtype=bool)

    # Find the start and end indices of NaN sequences
    nan_diff = np.diff(np.concatenate(([0], np.isnan(data[f'Probe_{BHE}_V_dot'].values), [0])))
    nan_starts = np.where(nan_diff == 1)[0]
    nan_ends = np.where(nan_diff == -1)[0]

    # Apply the condition for NaN sequences longer than min_gap_size, plus the next nsteps positions
    for start, end in zip(nan_starts, nan_ends):
        if end - start > min_gap_size:
            mask_nan_volflow[start:min(end + nsteps, len(data[f'Probe_{BHE}_V_dot'].values))] = True

    # Combine the zero flow rate mask and the NaN mask
    combined_mask = mask_nan_volflow | mask_volflow

    # Find indices where combined_mask is True
    indices = np.where(combined_mask)[0]

    # Set mask to True for these indices and the next nsteps
    for idx in indices:
        mask[idx:idx + nsteps + 1] = True

    # Ensure the mask does not go out of bounds
    return mask[:len(data[f'Probe_{BHE}_T_in'].values)]


# time to mask after a noflow or datagap period (depending on pipelength) - calculated in calculate_fluid_travel_time.ipynb
MASKING_TIMES = {'01': 625.36,
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
