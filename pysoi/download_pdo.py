"""Download Pacific Decadal Oscillation Data."""

import pandas as pd
import numpy as np
import io
from datetime import datetime
from .utils import check_response, abbr_month


def download_pdo():
    """
    Download Pacific Decadal Oscillation Data.
    
    The PDO index is derived as the leading principal of monthly SST anomalies in the North Pacific Ocean,
    poleward of 20N. The monthly mean global average SST anomalies are removed to separate this 
    pattern of variability from any "global warming" signal that may be present in the data.
    
    The NCEI PDO index is based on NOAA's extended reconstruction of SSTs (ERSST Version 4). 
    It is constructed by regressing the ERSST anomalies against the Mantua PDO index for their 
    overlap period, to compute a PDO regression map for the North Pacific ERSST anomalies. 
    The ERSST anomalies are then projected onto that map to compute the NCEI index. 
    The NCEI PDO index closely follows the Mantua PDO index.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Month: Month of record
        - Year: Year of record
        - PDO: Pacific Decadal Oscillation index
    
    References:
        Original PDO: https://oceanview.pfeg.noaa.gov/erddap/info/cciea_OC_PDO/index.html
    """
    # Construct the URL with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    pdo_link = f"https://oceanview.pfeg.noaa.gov/erddap/tabledap/cciea_OC_PDO.csv?time%2CPDO&time%3E=1900-01-01&time%3C={current_date}"
    
    # Get response
    response_text = check_response(pdo_link)
    
    # Read CSV
    # Skip the first two lines which contain metadata
    lines = response_text.splitlines()[2:]
    csv_text = '\n'.join(lines)
    
    # Parse CSV
    pdo = pd.read_csv(io.StringIO(csv_text), names=["Date", "PDO"])
    
    # Convert date string to datetime
    pdo['Date'] = pd.to_datetime(pdo['Date'])
    
    # Extract year
    pdo['Year'] = pdo['Date'].dt.year
    
    # Create Month as categorical from Date
    pdo['Month'] = abbr_month(pdo['Date'])
    
    # Select and return desired columns
    return pdo[["Year", "Month", "Date", "PDO"]]
