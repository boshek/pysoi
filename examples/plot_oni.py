#!/usr/bin/env python
"""
Example script to download and plot the Oceanic Nino Index (ONI).

This script demonstrates how to use the pysoi package to download ONI data
and create a simple visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os

# Add the parent directory to the path to import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the download_oni function from pysoi
from pysoi import download_oni

def main():
    """Download and plot ONI data."""
    print("Downloading ONI data...")
    oni = download_oni()
    
    print(f"Downloaded {len(oni)} records. Here's a sample:")
    print(oni.head())
    
    # Define colors for different phases
    colors = {
        'Warm Phase/El Nino': '#2c7fb8', 
        'Neutral Phase': '#7fcdbb',
        'Cool Phase/La Nina': '#edf8b1'
    }
    
    # Map phases to colors
    bar_colors = [colors.get(phase, '#7fcdbb') for phase in oni['phase']]
    
    # Create plot
    plt.figure(figsize=(15, 6))
    
    # Create the bar plot
    plt.bar(oni['Date'], oni['ONI'], color=bar_colors, width=30)
    
    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Oceanic Nino Index')
    plt.title('Oceanic Nino Index (ONI) Over Time')
    
    # Add grid and legend
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Create custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors['Warm Phase/El Nino'], label='Warm Phase/El Nino'),
        Patch(facecolor=colors['Neutral Phase'], label='Neutral Phase'),
        Patch(facecolor=colors['Cool Phase/La Nina'], label='Cool Phase/La Nina')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('oni_plot.png', dpi=300)
    
    print("Plot saved as 'oni_plot.png'")
    plt.show()

if __name__ == "__main__":
    main()
