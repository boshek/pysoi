"""Download Oceanic Nino Index data."""

import pandas as pd
import numpy as np
import io
from .utils import check_response, abbr_month


def download_oni():
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
    oni_link = "http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt"
    
    # Get response
    response_text = check_response(oni_link)
    
    # Read table - use sep='\s+' instead of delim_whitespace to avoid deprecation warning
    oni = pd.read_csv(io.StringIO(response_text), 
                      sep='\s+',
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
    
    # Create ONI month window - initialize as string type to avoid dtype issues
    oni['ONI_month_window'] = pd.Series(np.nan, index=oni.index, dtype='object')
    
    # Get first letter of each month
    month_abbrs = oni['Month'].astype(str).str[0]
    
    # Fill in the ONI month window values
    for i in range(1, len(oni) - 1):
        oni.loc[i, 'ONI_month_window'] = month_abbrs.iloc[i-1] + month_abbrs.iloc[i] + month_abbrs.iloc[i+1]
    
    # Assign phase - ensure all elements are strings to avoid dtype issues
    conditions = [
        (oni['ONI'] <= -0.5),
        (oni['ONI'] >= 0.5),
        (oni['ONI'] > -0.5) & (oni['ONI'] < 0.5)
    ]
    choices = ['Cool Phase/La Nina', 'Warm Phase/El Nino', 'Neutral Phase']
    
    # Use Series.mask method to avoid numpy select dtype issues
    oni['phase'] = pd.Series('', index=oni.index, dtype='object')
    
    # Apply conditions one by one
    for condition, choice in zip(conditions, choices):
        oni.loc[condition, 'phase'] = choice
    
    # Convert to categorical
    oni['phase'] = pd.Categorical(oni['phase'])
    
    # Select and return desired columns
    return oni[["Year", "Month", "Date", "dSST3.4", "ONI", "ONI_month_window", "phase"]]
