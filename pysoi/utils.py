"""Utility functions for the pysoi package."""

import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime
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


def download_with_cache(use_cache, file_path, download_function):
    """
    Download data with optional caching.
    
    Args:
        use_cache: Whether to use cache
        file_path: Path to cache file
        download_function: Function to download the data
        
    Returns:
        DataFrame: Downloaded data
    """
    # Check if cache file exists and should be used
    if use_cache and file_path and os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=['Date'])
    
    # Check internet connection and download data
    try:
        data = download_function()
    except (requests.ConnectionError, ConnectionError):
        print("A working internet connection is required to download and import the climate indices.")
        return None
    
    # Write to cache file if specified
    if file_path:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        data.to_csv(file_path, index=False)
    
    return data
