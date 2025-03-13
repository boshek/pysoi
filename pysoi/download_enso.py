"""Download Southern Oscillation Index and Oceanic Nino Index data."""

import pandas as pd
from .download_oni import download_oni
from .download_soi import download_soi
from .download_npgo import download_npgo


def download_enso(climate_idx="all", create_csv=False):
    """
    Download Southern Oscillation Index and Oceanic Nino Index data.
    
    The Southern Oscillation Index is defined as the standardized difference 
    between barometric readings at Darwin, Australia and Tahiti. The Oceanic 
    Nino Index is average sea surface temperature in the Nino 3.4 region 
    (120W to 170W) averaged over three months. Phases are categorized by 
    Oceanic Nino Index:
    - Warm phase of El Nino/Southern Oscillation when 3-month average 
      sea-surface temperature departure of positive 0.5 degC
    - Cool phase of La Nina/Southern Oscillation when 3-month average 
      sea-surface temperature departure of negative 0.5 degC
    - Neutral phase is defined as when the three month temperature average 
      is between +0.5 and -0.5 degC
    
    Args:
        climate_idx: Choose which ENSO related climate index to output. 
                     Options are "soi" (the Southern Oscillation Index), 
                     "oni" (the Oceanic Nino Index), "npgo" (the North 
                     Pacific Gyre Oscillation) and "all". "all" outputs 
                     each supported index variable as a slimmer dataset.
        create_csv: Whether to create a local copy of the data named "ENSO_Index.csv".
    
    Returns:
        DataFrame with columns (depending on which indices are selected):
        - Date: Date object
        - Month: Month of record
        - Year: Year of record
        - ONI: Oceanic Oscillation Index
        - phase: ENSO phase
        - SOI: Southern Oscillation Index
        - NPGO: North Pacific Gyre Oscillation
    """
    valid_options = ["all", "soi", "oni", "npgo"]
    if climate_idx not in valid_options:
        raise ValueError(f"climate_idx must be one of {valid_options}")
        
    if climate_idx == "soi":
        return download_soi()
    
    if climate_idx == "oni":
        return download_oni()
    
    if climate_idx == "npgo":
        return download_npgo()
    
    if climate_idx == "all":
        # Join index data
        oni_df = download_oni()
        soi_df = download_soi()
        npgo_df = download_npgo()
        
        # Merge data
        enso = pd.merge(oni_df, soi_df, on=["Date", "Year", "Month"], how="outer")
        enso = pd.merge(enso, npgo_df, on=["Date", "Year", "Month"], how="outer")
        
        # Select desired columns
        enso = enso[["Date", "Year", "Month", "ONI", "phase", "SOI", "NPGO"]]
        
        # Create CSV if requested
        if create_csv:
            enso.to_csv("ENSO_Index.csv", index=False)
        
        return enso
