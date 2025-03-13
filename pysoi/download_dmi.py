"""Download Dipole Mode Index (DMI) data."""

import pandas as pd
import numpy as np
import io
import calendar
import re
from .utils import check_response, abbr_month


def download_dmi():
    """
    Download Dipole Mode Index (DMI).
    
    Intensity of the IOD is represented by anomalous SST gradient 
    between the western equatorial Indian Ocean (50E-70E and 10S-10N) and the 
    south eastern equatorial Indian Ocean (90E-110E and 10S-0N). 
    This gradient is named as Dipole Mode Index (DMI). 
    When the DMI is positive then, the phenomenon is refereed as the positive
    IOD and when it is negative, it is refereed as negative IOD.
    
    Returns:
        DataFrame with columns:
        - Year: Year of record
        - Month: Month of record
        - Date: Date object
        - DMI: Dipole Mode Index
    
    References:
        https://psl.noaa.gov/gcos_wgsp/Timeseries/DMI/
    """
    dmi_link = "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data"
    
    # Get response
    response_text = check_response(dmi_link)
    
    # Parse the header to get years range
    lines = response_text.splitlines()
    header = lines[0].strip()
    years_match = re.findall(r'\d{4}', header)
    
    if len(years_match) >= 2:
        start_year = int(years_match[0])
        end_year = int(years_match[1])
    else:
        # If can't parse header, use a reasonable default
        start_year = 1850
        end_year = 2025
    
    # Get month abbreviations
    months = list(calendar.month_abbr)[1:]  # Skip the empty first element
    
    # Create a list to store data
    data_list = []
    
    # Process each data line
    for line in lines[1:]:
        if not line.strip():
            continue
            
        values = line.split()
        if len(values) < 13:  # Year + 12 months
            continue
            
        try:
            year = int(values[0])
            
            for i, month_idx in enumerate(range(1, 13), 1):
                if month_idx < len(values):
                    dmi_value = values[month_idx]
                    
                    # Convert to float, handle missing values
                    try:
                        dmi_value = float(dmi_value)
                        if dmi_value == -9999.000:  # Missing value indicator
                            dmi_value = np.nan
                    except ValueError:
                        dmi_value = np.nan
                    
                    # Create a record
                    date = pd.to_datetime(f"{year}-{i}-01")
                    
                    data_list.append({
                        'Year': year,
                        'Month': months[i-1],
                        'Date': date,
                        'DMI': dmi_value
                    })
        except (ValueError, IndexError):
            # Skip lines that can't be parsed
            continue
    
    # Create DataFrame
    dmi = pd.DataFrame(data_list)
    
    # Convert Month to categorical
    dmi['Month'] = pd.Categorical(dmi['Month'], categories=months, ordered=True)
    
    # Sort by date
    dmi = dmi.sort_values('Date').reset_index(drop=True)
    
    # Select and return desired columns
    return dmi[["Year", "Month", "Date", "DMI"]]
