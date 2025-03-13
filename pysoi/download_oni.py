"""Download Oceanic Nino Index data."""

import pandas as pd
import numpy as np
import io
from .utils import check_response, abbr_month, download_with_cache


def download_oni_data():
    """
    Download ONI data from NOAA.
    
    Returns:
        DataFrame: ONI data
    """
    oni_link = "http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt"
    
    # Get response
    response_text = check_response(oni_link)
    
    # Read table
    oni = pd.read_csv(io.StringIO(response_text), 
                      delim_whitespace=True,
                      names=["Year", "Month", "TOTAL", "ClimAdjust", "dSST3.4"],
                      skiprows=1)
    
    # Keep only relevant columns
    oni = oni[["Year", "Month", "dSST3.4"]]
    
    # Create Date column from Year and Month
    oni['Date'] = pd.to_datetime(oni['Year'].astype(str) + '-' + oni['Month'].astype(str) + '-01')
    
    # Create Month label
    oni['Month'] = abbr_month(oni['Date'])
    
    # Create 3 month average window
    oni['ONI'] = oni['dSST3.4'].rolling(window=3, center=True).mean()
    
    # Create ONI month window
    month_abbrs = oni['Month'].astype(str).str[0]
    oni['ONI_month_window'] = np.nan
    
    for i in range(1, len(oni) - 1):
        oni.loc[i, 'ONI_month_window'] = month_abbrs.iloc[i-1] + month_abbrs.iloc[i] + month_abbrs.iloc[i+1]
    
    # Assign phase
    conditions = [
        (oni['ONI'] <= -0.5),
        (oni['ONI'] >= 0.5),
        (oni['ONI'] > -0.5) & (oni['ONI'] < 0.5)
    ]
    choices = ['Cool Phase/La Nina', 'Warm Phase/El Nino', 'Neutral Phase']
    oni['phase'] = pd.Categorical(np.select(conditions, choices, default=np.nan))
    
    # Select and return desired columns
    return oni[["Year", "Month", "Date", "dSST3.4", "ONI", "ONI_month_window", "phase"]]


def download_oni(use_cache=False, file_path=None):
    """
    Download Oceanic Nino Index data.
    
    The Oceanic Nino Index is average sea surface temperature in the Nino 3.4 
    region (120W to 170W) averaged over three months. Phases are categorized by 
    Oceanic Nino Index:
    - Warm phase of El Nino/Southern Oscillation when 3-month average 
      sea-surface temperature departure of positive 0.5 degC
    - Cool phase of La Nina/Southern Oscillation when 3-month average 
      sea-surface temperature departure of negative 0.5 degC
    - Neutral phase is defined as when the three month temperature average 
      is between +0.5 and -0.5 degC
    
    Args:
        use_cache: Whether to use cache. If True, results will be cached in 
                   memory if file_path is None or on disk if file_path is not None.
        file_path: Path to file to save the data. If use_cache is False but file_path
                   is not None, the results will be downloaded and saved on disk.
    
    Returns:
        DataFrame with columns:
        - Date: Date object 
        - Month: Month of record
        - Year: Year of record
        - ONI: Oceanic Oscillation Index
        - ONI_month_window: 3 month period over which the ONI is calculated
        - phase: ENSO phase
    
    References:
        https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml
    """
    return download_with_cache(use_cache, file_path, download_oni_data)
