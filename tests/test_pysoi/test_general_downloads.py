"""General tests for all download functions."""

import pytest
import pandas as pd
import importlib
from pysoi import (
    download_oni, download_ao, download_nao, download_soi, 
    download_mei, download_npgo, download_aao, download_pdo, 
    download_dmi, download_asymsam_monthly, download_asymsam_daily
)

# List of download functions to test
FUNCTIONS = [
    "download_oni", "download_ao", "download_nao", "download_soi", 
    "download_mei", "download_npgo", "download_aao", "download_pdo", 
    "download_dmi", "download_asymsam_monthly"
]

@pytest.mark.parametrize("function_name", FUNCTIONS)
def test_download_returns_dataframe(function_name):
    """Test that all download functions return a DataFrame."""
    # Skip test if no internet connection
    try:
        # Get the function by name
        function = globals()[function_name]
        
        # Call the function
        result = function()
        
        # Check that the result is a DataFrame
        assert isinstance(result, pd.DataFrame), f"{function_name} did not return a DataFrame"
    except ConnectionError:
        pytest.skip("No internet connection")


def test_download_enso():
    """Test that the download_enso function works with different indices."""
    from pysoi import download_enso
    
    # Skip test if no internet connection
    try:
        # Test with 'all' option
        result_all = download_enso('all')
        assert isinstance(result_all, pd.DataFrame)
        assert all(col in result_all.columns for col in ["ONI", "SOI", "NPGO"])
        
        # Test with 'oni' option
        result_oni = download_enso('oni')
        assert isinstance(result_oni, pd.DataFrame)
        assert "ONI" in result_oni.columns
    except ConnectionError:
        pytest.skip("No internet connection")
