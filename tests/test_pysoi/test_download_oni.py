"""Test for the download_oni function."""

import pytest
import pandas as pd
from pysoi import download_oni


def test_download_oni():
    """Test that download_oni returns a DataFrame."""
    # Skip test if no internet connection
    try:
        oni = download_oni()
        assert isinstance(oni, pd.DataFrame)
    except ConnectionError:
        pytest.skip("No internet connection")


def test_oni_columns():
    """Test that the ONI data has the correct columns."""
    # Skip test if no internet connection
    try:
        oni = download_oni()
        expected_columns = ["Year", "Month", "Date", "dSST3.4", "ONI", "ONI_month_window", "phase"]
        assert all(col in oni.columns for col in expected_columns)
    except ConnectionError:
        pytest.skip("No internet connection")


def test_oni_window_na():
    """Test that the first and last rows of ONI_month_window are NA."""
    # Skip test if no internet connection
    try:
        oni = download_oni()
        assert pd.isna(oni['ONI_month_window'].iloc[0])
        assert pd.isna(oni['ONI_month_window'].iloc[-1])
    except ConnectionError:
        pytest.skip("No internet connection")
