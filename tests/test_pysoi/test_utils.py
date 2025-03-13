"""Tests for utility functions."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from pysoi.utils import abbr_month, check_response, download_with_cache


def test_abbr_month():
    """Test the abbr_month function."""
    # Create test dates
    dates = pd.to_datetime(['2022-01-01', '2022-02-01', '2022-03-01', '2022-12-01'])
    
    # Call the function
    result = abbr_month(dates)
    
    # Check that the result is categorical
    assert pd.api.types.is_categorical_dtype(result)
    
    # Check that the months are correct
    expected = ['Jan', 'Feb', 'Mar', 'Dec']
    assert list(result) == expected


def test_abbr_month_error():
    """Test that abbr_month raises an error with non-datetime input."""
    # Create non-datetime input
    not_dates = pd.Series(['Jan', 'Feb', 'Mar'])
    
    # Check that the function raises a TypeError
    with pytest.raises(TypeError):
        abbr_month(not_dates)


def test_check_response():
    """Test the check_response function with a valid URL."""
    # Skip this test if no internet connection
    try:
        # Use a reliable URL that should always be available
        url = "https://www.google.com"
        
        # Call the function
        result = check_response(url)
        
        # Check that the result is a string
        assert isinstance(result, str)
    except ConnectionError:
        pytest.skip("No internet connection")


def test_check_response_error():
    """Test that check_response raises an error with an invalid URL."""
    # Skip this test if internet connection works too well
    try:
        # Use a URL that should not exist
        url = "https://this-url-does-not-exist-123456789.com"
        
        # Check that the function raises an error
        with pytest.raises(Exception):
            check_response(url)
    except Exception:
        pytest.skip("Could connect to non-existent URL")


def test_download_with_cache():
    """Test the download_with_cache function."""
    import tempfile
    import os
    
    # Create a mock download function
    def mock_download():
        return pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    
    # Create a temporary file for caching
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        temp_path = temp.name
    
    try:
        # Download data with caching enabled
        data1 = download_with_cache(True, temp_path, mock_download)
        
        # Check that the file exists
        assert os.path.exists(temp_path)
        
        # Modify the mock function to return different data
        def mock_download_different():
            return pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
        
        # Download data again with caching enabled - should get the cached data
        data2 = download_with_cache(True, temp_path, mock_download_different)
        
        # Data should be the same as the first download
        pd.testing.assert_frame_equal(data1, data2)
        
        # Download without cache - should get the new data
        data3 = download_with_cache(False, None, mock_download_different)
        
        # Data should be different
        with pytest.raises(AssertionError):
            pd.testing.assert_frame_equal(data1, data3)
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
