"""Download Asymmetric and Symmetric SAM indices."""

import pandas as pd
import numpy as np
import io
import requests


def download_asymsam_monthly():
    """
    Download monthly Asymmetric and Symmetric SAM indices.
    
    The Asymmetric and Symmetric SAM indices are computed as the 
    projection of geopotential height anomalies onto the zonally asymmetric and 
    zonally symmetric parts of the SAM field. 
    The detailed methodology can be found in Campitelli et al. (2022).
    
    Returns:
        DataFrame with columns:
        - Lev: Atmospheric level in hPa
        - Date: Date object
        - Index: Type of index. Either "sam", "ssam" or "asam"
        - Value: Value of the index
        - Value_normalized: Value of the index normalized by the standard deviation of the index
    
    References:
        Campitelli, E., Díaz, L. B., & Vera, C. (2022). Assessment of zonally symmetric 
        and asymmetric components of the Southern Annular Mode using a novel approach. 
        Climate Dynamics, 58(1), 161–178. https://doi.org/10.1007/s00382-021-05896-5
    """
    asymsam_monthly_link = "https://www.cima.fcen.uba.ar/~elio.campitelli/asymsam/data/sam_monthly.csv"
    
    # Read the CSV file directly
    try:
        data = pd.read_csv(asymsam_monthly_link, 
                          dtype={'Lev': 'int32', 'Index': 'category', 'Value': 'float64', 'Value_normalized': 'float64'},
                          parse_dates=['Date'])
        
        # Ensure Index is categorical with correct levels
        data['Index'] = pd.Categorical(data['Index'], categories=['sam', 'ssam', 'asam'], ordered=False)
        
        return data
    except Exception as e:
        print(f"Error downloading ASYMSAM monthly data: {e}")
        return None


def download_asymsam_daily(levels=700):
    """
    Download daily Asymmetric and Symmetric SAM indices.
    
    The Asymmetric and Symmetric SAM indices are computed as the 
    projection of geopotential height anomalies onto the zonally asymmetric and 
    zonally symmetric parts of the SAM field. 
    The detailed methodology can be found in Campitelli et al. (2022).
    
    Args:
        levels: Atmospheric levels in hPa to download. Either a list of levels or "all".
               Available levels are: 1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175,
               200, 225, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800,
               825, 850, 875, 900, 925, 950, 975 and 1000.
    
    Returns:
        DataFrame with columns:
        - Lev: Atmospheric level in hPa
        - Date: Date object
        - Index: Type of index. Either "sam", "ssam" or "asam"
        - Value: Value of the index
        - R.squared: The variance explained by the index
    
    References:
        Campitelli, E., Díaz, L. B., & Vera, C. (2022). Assessment of zonally symmetric 
        and asymmetric components of the Southern Annular Mode using a novel approach. 
        Climate Dynamics, 58(1), 161–178. https://doi.org/10.1007/s00382-021-05896-5
    """
    available_levels = [1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 
                      175, 200, 225, 250, 300, 350, 400, 450, 500, 550, 600, 
                      650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 
                      975, 1000]
    
    # Convert to list if single level was provided
    if not isinstance(levels, list) and levels != "all":
        levels = [levels]
    
    # Use all available levels if specified
    if levels == "all":
        levels = available_levels
    
    # Check for invalid levels
    bad_levels = [level for level in levels if level not in available_levels]
    if bad_levels:
        raise ValueError(f"Invalid levels: {', '.join(map(str, bad_levels))}\n"
                         f"Valid levels are: {', '.join(map(str, available_levels))}")
    
    # Base URL for data
    root_link = "https://www.cima.fcen.uba.ar/~elio.campitelli/asymsam/data/sam_level/"
    
    # Initialize list to store data for each level
    all_data = []
    
    # Download data for each requested level
    for level in levels:
        print(f"Downloading level: {level}")
        link = f"{root_link}sam_{level}hPa.csv"
        
        try:
            # Read data
            data = pd.read_csv(link, 
                              dtype={'Lev': 'int32', 'Index': 'category', 'Value': 'float64', 'R.squared': 'float64'},
                              parse_dates=['Date'])
            
            # Drop any extra columns
            if 'dump' in data.columns:
                data = data.drop(columns=['dump'])
                
            all_data.append(data)
        except Exception as e:
            print(f"Error downloading level {level}: {e}")
    
    # Combine all data
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Ensure Index is categorical with correct levels
        combined_data['Index'] = pd.Categorical(combined_data['Index'], 
                                               categories=['sam', 'ssam', 'asam'], 
                                               ordered=False)
        
        return combined_data
    else:
        return None
