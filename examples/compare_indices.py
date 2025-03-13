#!/usr/bin/env python
"""
Example script to download and compare multiple climate indices.

This script demonstrates how to use the pysoi package to download multiple
climate indices and compare them in a visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os
import numpy as np

# Add the parent directory to the path to import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from pysoi
from pysoi import download_enso

def main():
    """Download and plot multiple climate indices."""
    print("Downloading ENSO data (ONI, SOI, NPGO)...")
    enso = download_enso(climate_idx="all")
    
    print(f"Downloaded {len(enso)} records. Here's a sample:")
    print(enso.head())
    
    # Create plot
    fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
    # Filter to the common time period
    # Get start and end dates with data for all indices
    mask = ~enso[['ONI', 'SOI', 'NPGO']].isna().any(axis=1)
    common_data = enso[mask].copy()
    
    if len(common_data) > 0:
        # Plot ONI
        ax1 = axes[0]
        ax1.plot(common_data['Date'], common_data['ONI'], 'r-', linewidth=1.5)
        ax1.fill_between(common_data['Date'], common_data['ONI'], 0, 
                         where=common_data['ONI'] > 0, alpha=0.3, color='red')
        ax1.fill_between(common_data['Date'], common_data['ONI'], 0, 
                         where=common_data['ONI'] < 0, alpha=0.3, color='blue')
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.set_ylabel('ONI')
        ax1.set_title('Oceanic Nino Index (ONI)')
        
        # Plot SOI
        ax2 = axes[1]
        ax2.plot(common_data['Date'], common_data['SOI'], 'b-', linewidth=1.5)
        ax2.fill_between(common_data['Date'], common_data['SOI'], 0, 
                        where=common_data['SOI'] > 0, alpha=0.3, color='blue')
        ax2.fill_between(common_data['Date'], common_data['SOI'], 0, 
                        where=common_data['SOI'] < 0, alpha=0.3, color='red')
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.set_ylabel('SOI')
        ax2.set_title('Southern Oscillation Index (SOI)')
        
        # Plot NPGO
        ax3 = axes[2]
        ax3.plot(common_data['Date'], common_data['NPGO'], 'g-', linewidth=1.5)
        ax3.fill_between(common_data['Date'], common_data['NPGO'], 0, 
                        where=common_data['NPGO'] > 0, alpha=0.3, color='green')
        ax3.fill_between(common_data['Date'], common_data['NPGO'], 0, 
                        where=common_data['NPGO'] < 0, alpha=0.3, color='orange')
        ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax3.set_ylabel('NPGO')
        ax3.set_title('North Pacific Gyre Oscillation (NPGO)')
        
        # Format the x-axis
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax3.xaxis.set_major_locator(mdates.YearLocator(5))
        ax3.set_xlabel('Date')
        
        # Add grid
        for ax in axes:
            ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Calculate correlations
        oni_soi_corr = common_data['ONI'].corr(common_data['SOI'])
        oni_npgo_corr = common_data['ONI'].corr(common_data['NPGO'])
        soi_npgo_corr = common_data['SOI'].corr(common_data['NPGO'])
        
        # Add correlation text
        fig.text(0.01, 0.01, f"Correlations: ONI-SOI: {oni_soi_corr:.2f}, ONI-NPGO: {oni_npgo_corr:.2f}, SOI-NPGO: {soi_npgo_corr:.2f}")
        
        # Save the plot
        plt.tight_layout()
        plt.savefig('climate_indices_comparison.png', dpi=300)
        
        print("Plot saved as 'climate_indices_comparison.png'")
        plt.show()
    else:
        print("No common time period found with data for all indices.")

if __name__ == "__main__":
    main()
