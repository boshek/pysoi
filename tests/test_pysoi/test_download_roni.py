"""Test for the download_roni function."""

import pytest
import pandas as pd
from pysoi import download_roni


def test_download_roni():
    """Test that download_roni returns a DataFrame."""
    # Skip test if no internet connection
    try:
        roni = download_roni()
        assert isinstance(roni, pd.DataFrame)
    except ConnectionError:
        pytest.skip("No internet connection")


def test_roni_columns():
    """Test that the RONI data has the correct columns."""
    # Skip test if no internet connection
    try:
        roni = download_roni()
        expected_columns = ['Year', 'Season', 'Month', 'Date', 'RONI', 'phase']
        assert all(col in roni.columns for col in expected_columns)
    except ConnectionError:
        pytest.skip("No internet connection")
