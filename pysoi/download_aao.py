"""Download Antarctic Oscillation data."""

import pandas as pd
import numpy as np
import io
from .utils import check_response, abbr_month


def download_aao():
    """
    Download Antarctic Oscillation data.
    
    Projection of the monthly 700 hPa anomaly height field south of 20°S on the first EOF obtained
    from the monthly 700 hPa height anomaly.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Year: Year of record
        - Month: Month of record
        - AAO: Antarctic Oscillation
    
    References:
        https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao.shtml
    """
    aao_link = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/monthly.aao.index.b79.current.ascii"
    
    # Get response
    response_text = check_response(aao_link)
    
    # Create a list to store data
    data_list = []
    
    # Parse line by line
    for line in response_text.splitlines():
        if not line.strip():
            continue
        
        try:
            # Format is YYYY MM AAO with fixed width
            if len(line) < 10:
                continue
                
            year = int(line[:5].strip())
            month = int(line[5:10].strip())
            aao_value = float(line[10:].strip())
            
            # Create date
            date = pd.to_datetime(f"{year}-{month:02d}-01")
            
            data_list.append({
                'Year': year,
                'Month': date.strftime('%b'),
                'Date': date,
                'AAO': aao_value
            })
        except (ValueError, IndexError):
            # Skip lines that can't be parsed
            continue
    
    # Create DataFrame
    aao = pd.DataFrame(data_list)
    
    # Convert Month to categorical
    aao['Month'] = abbr_month(aao[['Date']])
    
    # Sort by date
    aao = aao.sort_values('Date').reset_index(drop=True)
    
    # Select and return desired columns
    return aao[["Year", "Month", "Date", "AAO"]]
