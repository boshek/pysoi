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
    
    # Read table using sep instead of delim_whitespace to avoid deprecation warning
    npgo = pd.read_csv(io.StringIO(clean_text), 
                       sep=r'\s+',
                       names=["Year", "Month", "NPGO"])
    
    # Ensure Year and Month are integers
    npgo['Year'] = npgo['Year'].astype(int)
    npgo['Month'] = npgo['Month'].astype(int)
    
    # Create Date column with proper formatting
    npgo['Date'] = pd.to_datetime(
        pd.Series([f"{year}-{month:02d}-01" for year, month in zip(npgo['Year'], npgo['Month'])])
    )
    
    # Create Month label
    npgo['Month'] = abbr_month(npgo['Date'])
    
    # Select and return desired columns
    return npgo[["Year", "Month", "Date", "NPGO"]]
