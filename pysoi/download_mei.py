"""Download Multivariate ENSO Index Version 2 (MEI.v2)."""

import pandas as pd
import numpy as np
import io
import re
from .utils import check_response, download_with_cache


def download_mei_data():
    """
    Download Multivariate ENSO Index Version 2 (MEI.v2) data.
    
    Returns:
        DataFrame: MEI data
    """
    mei_link = "https://www.esrl.noaa.gov/psd/enso/mei/data/meiv2.data"
    
    # Get response
    response_text = check_response(mei_link)
    
    # Parse the header to get years range
    lines = response_text.splitlines()
    header = lines[0].strip()
    years_match = re.findall(r'\d{4}', header)
    
    if len(years_match) >= 2:
        start_year = int(years_match[0])
        end_year = int(years_match[1])
    else:
        # If can't parse header, use a reasonable default
        # This is a fallback and shouldn't normally be triggered
        start_year = 1979
        end_year = 2023
    
    # Define bi-monthly seasons
    months = ["DJ", "JF", "FM", "MA", "AM", "MJ", "JJ", "JA", "AS", "SO", "ON", "ND"]
    
    # Create a list to store data
    data_list = []
    
    # Process each data line
    for line in lines[1:]:
        if not line.strip():
            continue
            
        values = line.split()
        if len(values) < 13:  # Year + 12 bi-monthly values
            continue
            
        try:
            year = int(values[0])
            
            for i, month_idx in enumerate(range(1, 13)):
                if month_idx < len(values):
                    mei_value = values[month_idx]
                    
                    # Convert to float, handle missing values
                    try:
                        mei_value = float(mei_value)
                        if mei_value == -999.00:  # Missing value indicator
                            mei_value = np.nan
                    except ValueError:
                        mei_value = np.nan
                    
                    # Determine the month number based on bi-monthly code
                    # This approximates the date by using the first month
                    month_num = i + 1
                    if month_num > 12:
                        month_num = 12  # Max is December
                        
                    # Create a record
                    date = pd.to_datetime(f"{year}-{month_num}-01")
                    
                    # Determine phase based on MEI value
                    if mei_value <= -0.5:
                        phase = "Cool Phase/La Nina"
                    elif mei_value >= 0.5:
                        phase = "Warm Phase/El Nino"
                    else:
                        phase = "Neutral Phase"
                    
                    data_list.append({
                        'Year': year,
                        'Month': months[i],
                        'Date': date,
                        'MEI': mei_value,
                        'Phase': phase
                    })
        except (ValueError, IndexError):
            # Skip lines that can't be parsed
            continue
    
    # Create DataFrame
    mei = pd.DataFrame(data_list)
    
    # Convert Month to categorical
    mei['Month'] = pd.Categorical(mei['Month'], categories=months, ordered=True)
    
    # Convert Phase to categorical
    mei['Phase'] = pd.Categorical(
        mei['Phase'], 
        categories=["Cool Phase/La Nina", "Neutral Phase", "Warm Phase/El Nino"], 
        ordered=True
    )
    
    # Sort by date
    mei = mei.sort_values('Date').reset_index(drop=True)
    
    # Select and return desired columns
    return mei[["Year", "Month", "Date", "MEI", "Phase"]]


def download_mei(use_cache=False, file_path=None):
    """
    Download Multivariate ENSO Index Version 2 (MEI.v2).
    
    MEI.v2 is based on EOF analysis of level pressure, sea surface temperature,
    surface zonal winds, surface meridional winds, and Outgoing Longwave Radiation. 
    The analysis is conducted for 12 partially overlapping 2-month "seasons".
    
    Warm phase is defined as MEI index greater or equal to 0.5. Cold phase is 
    defined as MEI index lesser or equal to -0.5.
    
    Args:
        use_cache: Whether to use cache. If True, results will be cached in 
                   memory if file_path is None or on disk if file_path is not None.
        file_path: Path to file to save the data. If use_cache is False but file_path
                   is not None, the results will be downloaded and saved on disk.
    
    Returns:
        DataFrame with columns:
        - Date: Date object
        - Month: Bi-monthly season of record
        - Year: Year of record
        - MEI: Multivariate ENSO Index Version 2
        - Phase: ENSO phase
    
    References:
        https://psl.noaa.gov/enso/mei/
    """
    return download_with_cache(use_cache, file_path, download_mei_data)
