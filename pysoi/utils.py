"""Utility functions for the pysoi package."""

import pandas as pd
import numpy as np
import requests
import calendar


def abbr_month(date):
    """
    Extract an ordered factor of months from a date object.
    
    Args:
        date: pandas datetime or datetime object

    Returns:
        pandas.Series: Series with ordered categorical month abbreviations
    """
    if not pd.api.types.is_datetime64_any_dtype(date):
        raise TypeError("Not a pandas datetime object")
    
    month_abbrs = [calendar.month_abbr[i] for i in range(1, 13)]
    month_series = pd.Series(date.dt.strftime('%b'), index=date.index)
    
    return pd.Categorical(month_series, categories=month_abbrs, ordered=True)


def check_response(url):
    """
    Check the response from server and return content if successful.
    
    Args:
        url: URL to check
        
    Returns:
        Response content as text if successful
        
    Raises:
        Exception: If response status code is not 200 or if server is unavailable
    """
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError(f"Non successful http request. Target server returning a {response.status_code} error code")
        
        if "shutdown" in response.url:
            raise RuntimeError("Data source is currently unavailable due to a US government shutdown")
        
        return response.text
    except requests.ConnectionError:
        raise ConnectionError("A working internet connection is required to download and import the climate indices.")

    
def season_to_month(season: str) -> int:
    """
    From a 3-letter season code, extract the middle month and return it as an integer.

    This method only accepts length 3 strings, so seasons like 'DJF' 
    will return 1 for January, but does not accept season codes like 'JJAS'.
    """
    assert (type(season) == str and len(season) == 3), 'Please enter a 3-letter season code as a string'

    seasons_dict = {
        'DJF': 1,  
        'JFM': 2,  
        'FMA': 3,  
        'MAM': 4,
        'AMJ': 5,  
        'MJJ': 6,  
        'JJA': 7,  
        'JAS': 8,
        'ASO': 9,  
        'SON': 10, 
        'OND': 11, 
        'NDJ': 12,
    }

    assert season in seasons_dict, f'Season `{season}` not found in seasons.\nAvailable options:{list(seasons_dict.keys())}'

    return seasons_dict[season]
