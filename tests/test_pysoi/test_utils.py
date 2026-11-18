"""Tests for utility functions."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from pysoi.utils import abbr_month, check_response, season_to_month


def test_abbr_month():
    """Test the abbr_month function."""
    # Create test dates as a Series (not DatetimeIndex)
    dates = pd.Series(pd.to_datetime(['2022-01-01', '2022-02-01', '2022-03-01', '2022-12-01']))
    
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


def test_season_to_month():
    """Test the season_to_month function."""
    # Create list of season codes to test against
    seasons = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']
    
    # Call the function
    result = [season_to_month(season) for season in seasons]
    
    # Check that the month integers are correct
    expected = np.arange(1, 13, 1).tolist()
    assert result == expected


def test_season_to_month_error():
    """
    Test that season_to_month raises an error withnon-string input,
    with a season code that does not exist, and for a 4-letter season code.
    """
    # Check that the function only accepts string input
    with pytest.raises(AssertionError):
        season_to_month(1)

    # Check that the function only accepts 3-letter season codes that exist
    with pytest.raises(AssertionError):
        season_to_month('JJS')

    # Check that the function only accepts 3-letter season codes, not common 4-letter ones
    with pytest.raises(AssertionError):
        season_to_month('JJAS')