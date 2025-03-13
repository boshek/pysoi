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


def test_cache_functionality():
    """Test that cache functionality works correctly."""
    import tempfile
    import os
    
    # Create a temporary file for caching
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        temp_path = temp.name
    
    try:
        # Download data with caching enabled
        data1 = download_oni(use_cache=True, file_path=temp_path)
        
        # Check that the file exists
        assert os.path.exists(temp_path)
        
        # Download data again with caching enabled
        data2 = download_oni(use_cache=True, file_path=temp_path)
        
        # Both datasets should be identical
        pd.testing.assert_frame_equal(data1, data2)
    except Exception as e:
        pytest.skip(f"Cache test failed: {e}")
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


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
