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
