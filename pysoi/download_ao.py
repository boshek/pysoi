"""Download Arctic Oscillation data."""

import pandas as pd
import numpy as np
import io
import calendar
from .utils import check_response, abbr_month


def download_ao():
    """
    Download Arctic Oscillation data.
    
    Projection of the daily 1000 hPa anomaly height field north of 20°N on the first EOF obtained
    from the monthly 1000 hPa height anomaly.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Year: Year of record
        - Month: Month of record
        - AO: Arctic Oscillation
    
    References:
        https://www.ncdc.noaa.gov/teleconnections/ao/
    """
    ao_link = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii.table"
    
    # Get response
    response_text = check_response(ao_link)
    
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
                    ao_value = float(parts[month_idx])
                    date = pd.to_datetime(f"{year}-{i}-01")
                    
                    data_list.append({
                        'Year': year,
                        'Month': months[i-1],
                        'Date': date,
                        'AO': ao_value
                    })
                except ValueError:
                    # Skip invalid values
                    continue
    
    # Create DataFrame
    ao = pd.DataFrame(data_list)
    
    # Sort by date
    ao = ao.sort_values('Date').reset_index(drop=True)
    
    # Create Month label as categorical
    ao['Month'] = pd.Categorical(ao['Month'], categories=months, ordered=True)
    
    # Select and return desired columns
    return ao[["Year", "Month", "Date", "AO"]]
