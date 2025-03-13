"""Download North Atlantic Oscillation data."""

import pandas as pd
import numpy as np
import io
import calendar
from .utils import check_response, abbr_month


def download_nao():
    """
    Download North Atlantic Oscillation data.
    
    Surface sea-level pressure difference between the Subtropical (Azores) High and the Subpolar Low.
    
    Returns:
        DataFrame with columns:
        - Year: Year of record
        - Month: Month of record
        - NAO: North Atlantic Oscillation
    
    References:
        https://www.ncdc.noaa.gov/teleconnections/nao/
    """
    nao_link = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii.table"
    
    # Get response
    response_text = check_response(nao_link)
    
    # Parse the data
    months = list(calendar.month_abbr)[1:]  # Get month abbreviations
    
    # Read the fixed width file
    # This is tricky because the format isn't consistent, we'll handle line by line
    lines = response_text.splitlines()
    
    # Skip the header
    data_lines = lines[1:]
    
    data_list = []
    
    for line in data_lines:
        parts = line.split()
        if len(parts) < 13:  # Need year + 12 months
            continue
            
        year = int(parts[0])
        
        for i, month_idx in enumerate(range(1, 13), 1):
            if month_idx < len(parts):
                try:
                    nao_value = float(parts[month_idx])
                    date = pd.to_datetime(f"{year}-{i}-01")
                    
                    data_list.append({
                        'Year': year,
                        'Month': months[i-1],
                        'Date': date,
                        'NAO': nao_value
                    })
                except ValueError:
                    # Skip invalid values
                    continue
    
    # Create DataFrame
    nao = pd.DataFrame(data_list)
    
    # Sort by date
    nao = nao.sort_values('Date').reset_index(drop=True)
    
    # Create Month label as categorical
    nao['Month'] = pd.Categorical(nao['Month'], categories=months, ordered=True)
    
    # Select and return desired columns
    return nao[["Year", "Month", "NAO"]]
