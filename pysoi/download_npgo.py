"""Download North Pacific Gyre Oscillation data."""

import pandas as pd
import io
from .utils import check_response, abbr_month


def download_npgo():
    """
    Download North Pacific Gyre Oscillation data.
    
    North Pacific Gyre Oscillation data also known as the Victoria mode.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Year: Year of record
        - Month: Month of record
        - NPGO: North Pacific Gyre Oscillation
    
    References:
        http://www.oces.us/npgo/
    """
    npgo_link = "http://www.oces.us/npgo/data/NPGO.txt"
    
    # Get response
    response_text = check_response(npgo_link)
    
    # Remove comment lines
    data_lines = [line for line in response_text.splitlines() if not line.startswith('#')]
    clean_text = '\n'.join(data_lines)
    
    # Read table
    npgo = pd.read_csv(io.StringIO(clean_text), 
                       delim_whitespace=True,
                       names=["Year", "Month", "NPGO"])
    
    # Create Date column
    npgo['Date'] = pd.to_datetime(npgo['Year'].astype(str) + '-' + 
                                 npgo['Month'].astype(str) + '-01')
    
    # Create Month label
    npgo['Month'] = abbr_month(npgo['Date'])
    
    # Ensure Year is integer
    npgo['Year'] = npgo['Year'].astype(int)
    
    # Select and return desired columns
    return npgo[["Year", "Month", "Date", "NPGO"]]
