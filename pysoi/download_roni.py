"""Download Relative Oceanic Nino Index data."""

import pandas as pd
import numpy as np
import io
from .utils import abbr_month, check_response, season_to_month


def download_roni():
    """
    Download Relative Oceanic Nino Index data.
    
    The Relative Oceanic Nino Index (RONI) is the 3-month running mean of ERSST.v6 SST anomalies in the 
    Niño 3.4 region (5°N-5°S, 120°-170°W) with the average tropical mean (20°N-20°S) SST anomalies subtracted, 
    using a base period of 1991-2020. The difference is then adjusted so the variance equals the original Niño 3.4 index.    

    - Warm phase of El Nino / Southern Oscillation when 3-month average 
      sea-surface temperature departure of positive 0.5 degC
    - Cool phase of La Nina / Southern Oscillation when 3-month average 
      sea-surface temperature departure of negative 0.5 degC
    - Neutral phase is defined as when the three month temperature average 
      is between +0.5 and -0.5 degC

    Notice: the RONI is updated by the 5th of each month. Because of the high frequency filter applied to the ERSSTv6 data, 
    RONI values may change up to two months after the initial "real time" value is posted. Therefore, the most recent RONI values 
    should be considered an estimate.
    
    Returns:
        DataFrame with columns:
        - Date: Date object 
        - Month: Month of record
        - Year: Year of record
        - RONI: Oceanic Oscillation Index
        - RONI_month_window: 3 month period over which the RONI is calculated
        - phase: ENSO phase
    
    References:
        https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/
        https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml
    """
    roni_link = "https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt"
    
    # Get response
    response_text = check_response(roni_link)
    
    # Read table - use sep='\s+' instead of delim_whitespace to avoid deprecation warning
    roni = pd.read_csv(
        io.StringIO(response_text), 
        sep=r'\s+',
        names=['Season', 'Year', 'RONI'],
        skiprows=1
    )

    # Create Date column from Year and Season
    roni['month_num'] = roni['Season'].map(season_to_month)
    roni['Date'] = pd.to_datetime(roni['Year'].astype(str) + '-' + roni['month_num'].astype(str) + '-01')

    # Create Month label
    roni['Month'] = abbr_month(roni['Date'])

     # Assign phase - ensure all elements are strings to avoid dtype issues
    conditions = [
        (roni['RONI'] <= -0.5),
        (roni['RONI'] >=  0.5),
        (roni['RONI'] >  -0.5) & (roni['RONI'] < 0.5),
    ]
    choices = ['Cool Phase/La Nina', 'Warm Phase/El Nino', 'Neutral Phase']
    # https://numpy.org/doc/stable/reference/generated/numpy.select.html
    roni['phase'] = np.select(conditions, choices, default='')
    
    # Convert to categorical
    roni['phase'] = pd.Categorical(roni['phase'])

    # Select and return desired columns
    return roni[['Year', 'Season', 'Month', 'Date', 'RONI', 'phase']]
