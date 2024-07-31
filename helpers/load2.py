import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import List, Union, Optional

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_BHE_RANGE = np.arange(1, 41, 1)
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
    BHEs = prepare_bhe_list(BHEs)
    columns = get_columns(BHEs)
    data_dir = PREPARED_DATA_DIR if data_type == 'prepared' else RAW_DATA_DIR
    
    time_start_global = dt.strptime(start_date, TIME_FORMAT)
    time_end_global = dt.strptime(end_date, TIME_FORMAT)
    BHE_data = pd.concat(
        load_monthly_data(data_dir, time_start_global, time_end_global, columns, data_type)
    )
    
    BHE_data = BHE_data.loc[time_start_global:time_end_global]
    
    if masked:
        apply_mask(BHE_data, BHEs)
    
    return BHE_data

def prepare_bhe_list(BHEs: Optional[Union[List[Union[str, int]], np.ndarray, str, int]]) -> List[str]:
    if BHEs is None:
        BHEs = DEFAULT_BHE_RANGE
    elif not isinstance(BHEs, (list, np.ndarray)):
        BHEs = [BHEs]

    return [f'{int(bhe):02d}' if not isinstance(bhe, str) else bhe for bhe in BHEs]

def get_columns(BHEs: List[str]) -> List[str]:
    return [f'Probe_{BHE}_T_in' for BHE in BHEs] + \
           [f'Probe_{BHE}_T_out' for BHE in BHEs] + \
           [f'Probe_{BHE}_V_dot' for BHE in BHEs]

def load_monthly_data(data_dir: Path, start_date: dt, end_date: dt, columns: List[str], data_type: str) -> List[pd.DataFrame]:
    time_step = relativedelta(months=+1)
    time_current = start_date
    data_frames = []

    while time_current <= end_date:
        file_path = data_dir / f"ERC_data_{data_type}_{time_current.year}_{time_current.month:02d}.csv"
        data = pd.read_csv(file_path)
        data.index = pd.to_datetime(data['Time'], utc=True).tz_localize(None)
        
        data_frames.append(data if len(columns) == 120 else data[columns])
        
        time_current += time_step
    
    return data_frames

def apply_mask(data: pd.DataFrame, BHEs: List[str]) -> None:
    for BHE in BHEs:
        mask = create_BHE_data_mask(data, BHE)
        data.loc[mask, [f'Probe_{BHE}_T_in', f'Probe_{BHE}_T_out', f'Probe_{BHE}_V_dot']] = np.nan

def create_BHE_data_mask(data: pd.DataFrame, BHE: Union[int, str], timestep: int = 30) -> np.ndarray:
    BHE = f'{int(BHE):02d}' if isinstance(BHE, int) else BHE

    time_to_mask = MASKING_TIMES.get(BHE, 0)
    nsteps = -(-time_to_mask // timestep)  # Round up to the next integer
    min_gap_size = 20

    T_in_series = data[f'Probe_{BHE}_T_in'].values
    V_dot_series = data[f'Probe_{BHE}_V_dot'].values

    mask = np.zeros_like(T_in_series, dtype=bool)
    mask_volflow = V_dot_series < 0.5
    mask_nan_volflow = create_nan_mask(V_dot_series, min_gap_size, nsteps)

    combined_mask = mask_nan_volflow | mask_volflow
    indices = np.where(combined_mask)[0]

    for idx in indices:
        mask[idx:idx + nsteps + 1] = True

    return mask[:len(T_in_series)]

def create_nan_mask(series: np.ndarray, min_gap_size: int, nsteps: int) -> np.ndarray:
    mask_nan = np.zeros_like(series, dtype=bool)
    nan_diff = np.diff(np.concatenate(([0], np.isnan(series), [0])))
    nan_starts = np.where(nan_diff == 1)[0]
    nan_ends = np.where(nan_diff == -1)[0]

    for start, end in zip(nan_starts, nan_ends):
        if end - start > min_gap_size:
            mask_nan[start:min(end + nsteps, len(series))] = True

    return mask_nan



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

