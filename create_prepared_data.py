#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script reads raw data, processes it by masking non-representative periods,
specific time periods for certain columns, dealing with outliers, and resampling it
to a desired time interval. The processed data is then saved to a new directory.
"""

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from pathlib import Path
from typing import List, Tuple
from helpers import load

# Define constants
NEW_TIME_INTERVAL: str = '300s'  # Example: 1H for one hour, 300s for 5 min, etc. - see pandas documentation
MASK_WRONG_SENSOR_DATA: bool = True  # Whether to mask wrong sensor data
START_DATE: str = "2018-07-01 00:00:00"
END_DATE: str = "2024-06-30 23:59:59"
TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# Define global paths
RAW_DATA_PATH: Path = Path("data/raw_30s/")
PREPARED_DATA_PATH: Path = Path("data/prepared_5min/")

# Define periods and columns to mask
MASK_PERIODS: List[Tuple[str, str, str]] = [
    ("Probe_13_T_out", "2021-02-01", "2024-02-15"),
    ("Probe_35_T_in", "2019-08-01", "2024-02-15"),
    ("Probe_29_T_in", "2019-02-01", "2024-02-15"),
    ("Probe_33_T_in", "2019-07-01", "2024-02-15"),
    ("Probe_13_T_in", "2019-02-01", "2023-03-06"),
    ("Probe_26_T_in", "2018-07-01", "2024-06-30")
]

# Initialize time range
time_start_global = dt.strptime(START_DATE, TIME_FORMAT)
time_end_global = dt.strptime(END_DATE, TIME_FORMAT)
time_step = relativedelta(months=+1)
time_start = time_start_global

# Generate list of BHEs
BHEs: List[str] = [f'{x:02d}' for x in np.arange(1, 41, 1)]

def apply_custom_masks(data: pd.DataFrame, mask_periods: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """
    Apply custom masks to the specified columns and time periods.

    Parameters:
    data (pd.DataFrame): The dataframe containing the data.
    mask_periods (List[Tuple[str, str, str]]): List of tuples specifying (column, start_date, end_date).

    Returns:
    pd.DataFrame: The dataframe with applied masks.
    """
    for column, start_date, end_date in mask_periods:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        data.loc[(data.index >= start) & (data.index <= end), column] = np.nan
    return data

# Process data
while time_start <= time_end_global:
    print(time_start)
    # Load data
    loadname = RAW_DATA_PATH / f"ERC_data_raw_{time_start.year}_{time_start.month:02d}.csv"
    data = pd.read_csv(loadname)
    data.index = pd.to_datetime(data['Time'], utc=True)
    data.index = data.index.tz_localize(None)

    # Mask non-representative periods
    for BHE in BHEs:
        mask = load.create_BHE_data_mask(data, BHE)
        data.loc[mask, [f'Probe_{BHE}_T_in', f'Probe_{BHE}_T_out', f'Probe_{BHE}_V_dot']] = np.nan

    # Apply custom masks
    if MASK_WRONG_SENSOR_DATA:
        data = apply_custom_masks(data, MASK_PERIODS)

    # Resample data
    data = data.resample(NEW_TIME_INTERVAL).mean().round(2)

    # Save processed data
    output_name = PREPARED_DATA_PATH / f'ERC_data_prepared_{time_start.year}_{time_start.month:02d}.csv'
    data.to_csv(output_name)

    # Increment time_start by time_step
    time_start += time_step
