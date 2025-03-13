"""Download Southern Oscillation Index data."""

import pandas as pd
import numpy as np
import io
import re
from .utils import check_response, abbr_month
import calendar


def download_soi():
    """
    Download Southern Oscillation Index data.
    
    The Southern Oscillation Index is defined as the standardized difference 
    between barometric readings at Darwin, Australia and Tahiti.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Month: Month of record
        - Year: Year of record
        - SOI: Southern Oscillation Index
        - SOI_3MON_AVG: 3 Month Average Southern Oscillation Index
    
    References:
        https://www.cpc.ncep.noaa.gov/data/indices/soi
    """
    soi_link = "https://www.cpc.ncep.noaa.gov/data/indices/soi"
    
    # Get raw text data
    raw_text = check_response(soi_link)
    
    # Extract the relevant portion of the text
    raw_lines = raw_text.splitlines()
    start_idx = next(i for i, line in enumerate(raw_lines) if "STANDARDIZED" in line)
    table_start_idx = next(i for i, line in enumerate(raw_lines[start_idx:], start_idx) if "YEAR" in line)
    table_text = '\n'.join(raw_lines[table_start_idx:])
    
    # Parse the fixed width file
    months = list(calendar.month_abbr)[1:]  # Get month abbreviations
    
    # Create a list to store the data
    data_list = []
    
    # Parse the data
    for line in table_text.splitlines()[1:]:  # Skip the header
        if not line.strip():  # Skip empty lines
            continue
            
        # Extract values
        values = line.split()
        if len(values) < 13:  # Need year + 12 months
            continue
            
        year = int(values[0])
        
        for i, month_idx in enumerate(range(1, 13), 1):
            if month_idx < len(values):
                soi_value = values[month_idx]
                
                # Convert to float, handle missing values
                try:
                    soi_value = float(soi_value)
                    if soi_value == -999.9:  # Missing value indicator
                        soi_value = np.nan
                except ValueError:
                    soi_value = np.nan
                
                # Create a record
                month_name = months[i-1]
                date = pd.to_datetime(f"{year}-{i}-01")
                
                data_list.append({
                    'Year': year,
                    'Month': month_name,
                    'Date': date,
                    'SOI': soi_value
                })
    
    # Create DataFrame
    soi = pd.DataFrame(data_list)
    
    # Sort by date
    soi = soi.sort_values('Date').reset_index(drop=True)
    
    # Month as categorical
    soi['Month'] = abbr_month(soi['Date'])
    
    # Create 3-month moving average
    soi['SOI_3MON_AVG'] = soi['SOI'].rolling(window=3, center=True).mean()
    
    return soi[['Year', 'Month', 'Date', 'SOI', 'SOI_3MON_AVG']]
