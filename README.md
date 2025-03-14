# Download Multiple Indices


# PySOI - Climate Indices in Python

[![License: GPL
v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Python package to download and analyze climate indices including:

- Southern Oscillation Index (SOI)
- Oceanic Nino Index (ONI)
- North Pacific Gyre Oscillation (NPGO)
- North Atlantic Oscillation (NAO)
- Arctic Oscillation (AO)
- Antarctic Oscillation (AAO)
- Multivariate ENSO Index Version 2 (MEI)
- Pacific Decadal Oscillation (PDO)
- Dipole Mode Index (DMI)
- Asymmetric and Symmetric SAM indices (ASYMSAM)

## Installation

### From source

``` bash
git clone https://github.com/boshek/pysoi.git
cd pysoi
pip install -e .
```

## Usage

### Basic Usage

Download Oceanic Nino Index data:

``` python
from pysoi import download_oni
import pandas as pd

# Download ONI data
oni = download_oni()

# Display the first few rows
print(oni.head())
```

       Year Month       Date  dSST3.4       ONI ONI_month_window  \
    0  1950   Jan 1950-01-01    -1.62       NaN              NaN   
    1  1950   Feb 1950-02-01    -1.32 -1.336667              JFM   
    2  1950   Mar 1950-03-01    -1.07 -1.166667              FMA   
    3  1950   Apr 1950-04-01    -1.11 -1.183333              MAM   
    4  1950   May 1950-05-01    -1.37 -1.073333              AMJ   

                    phase  
    0                      
    1  Cool Phase/La Nina  
    2  Cool Phase/La Nina  
    3  Cool Phase/La Nina  
    4  Cool Phase/La Nina  

You can download multiple indices together:

``` python
from pysoi import download_enso

# Download ENSO-related indices (ONI, SOI, NPGO)
enso = download_enso(climate_idx="all")
```

## Available Functions

The package provides the following functions to download climate
indices:

| Function | Description |
|----|----|
| `download_oni()` | Oceanic Nino Index |
| `download_soi()` | Southern Oscillation Index |
| `download_npgo()` | North Pacific Gyre Oscillation |
| `download_nao()` | North Atlantic Oscillation |
| `download_ao()` | Arctic Oscillation |
| `download_aao()` | Antarctic Oscillation |
| `download_mei()` | Multivariate ENSO Index Version 2 |
| `download_pdo()` | Pacific Decadal Oscillation |
| `download_dmi()` | Dipole Mode Index |
| `download_asymsam_monthly()` | Monthly Asymmetric and Symmetric SAM indices |
| `download_asymsam_daily()` | Daily Asymmetric and Symmetric SAM indices |
| `download_enso()` | Combined ENSO-related indices (ONI, SOI, NPGO) |

All download functions accept these common parameters: - `use_cache`:
Whether to use cached data (default: False) - `file_path`: Optional path
to save/load cached data

## Climate Indices Information

### El Niño-Southern Oscillation (ENSO)

ENSO is one of the most important climate phenomena on Earth due to its
ability to change the global atmospheric circulation, which in turn,
influences temperature and precipitation across the globe. The Southern
Oscillation Index (SOI) and Oceanic Nino Index (ONI) are two key metrics
used to track ENSO.

- **Oceanic Nino Index (ONI)**: Average sea surface temperature in the
  Nino 3.4 region (120W to 170W) averaged over three months.
  - Warm phase (El Niño): ONI ≥ 0.5°C
  - Cool phase (La Niña): ONI ≤ -0.5°C
  - Neutral phase: -0.5°C \< ONI \< 0.5°C
- **Southern Oscillation Index (SOI)**: Standardized difference between
  barometric readings at Darwin, Australia and Tahiti.

### Other Indices

- **North Pacific Gyre Oscillation (NPGO)**: Measures changes in the
  North Pacific Ocean circulation.
- **North Atlantic Oscillation (NAO)**: Surface sea-level pressure
  difference between the Subtropical (Azores) High and the Subpolar Low.
- **Arctic Oscillation (AO)**: Projection of the daily 1000 hPa anomaly
  height field north of 20°N on the first EOF.
- **Antarctic Oscillation (AAO)**: Projection of the monthly 700 hPa
  anomaly height field south of 20°S on the first EOF.
- **Multivariate ENSO Index Version 2 (MEI)**: Based on EOF analysis of
  level pressure, sea surface temperature, surface winds, and Outgoing
  Longwave Radiation.
- **Pacific Decadal Oscillation (PDO)**: Leading principal component of
  monthly SST anomalies in the North Pacific Ocean.
- **Dipole Mode Index (DMI)**: Measures the intensity of the Indian
  Ocean Dipole (IOD).

## Examples

Example scripts are provided in the `examples` directory: -
`plot_oni.py`: Downloads and plots the Oceanic Nino Index -
`compare_indices.py`: Downloads and compares multiple climate indices

## Testing

Run the tests using pytest:

``` bash
# Run from the project root directory
python -m pytest tests/test_pysoi

# Or use the provided script
python tests/run_tests.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1.  Install development dependencies:

``` bash
pip install -e ".[dev]"
# or
pip install -r dev-requirements.txt
```

2.  Set up pre-commit hooks:

``` bash
pre-commit install
```

This will automatically run linters and code formatters on your commits.

## License

This project is licensed under the GNU General Public License v3.0 - see
the LICENSE file for details.

## Credits

This package is a Python adaptation of the R package `rsoi` by Sam
Albers. The original R package can be found at
<https://github.com/boshek/rsoi>.

## References

- Oceanic Nino Index (ONI):
  <https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml>
- Southern Oscillation Index (SOI):
  <https://www.cpc.ncep.noaa.gov/data/indices/soi>
- North Pacific Gyre Oscillation (NPGO): <http://www.oces.us/npgo/>
- North Atlantic Oscillation (NAO):
  <https://www.ncdc.noaa.gov/teleconnections/nao/>
- Arctic Oscillation (AO):
  <https://www.ncdc.noaa.gov/teleconnections/ao/>
- Antarctic Oscillation (AAO):
  <https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao.shtml>
- Multivariate ENSO Index Version 2 (MEI):
  <https://psl.noaa.gov/enso/mei/>
- Pacific Decadal Oscillation (PDO):
  <https://oceanview.pfeg.noaa.gov/erddap/info/cciea_OC_PDO/index.html>
- Dipole Mode Index (DMI):
  <https://psl.noaa.gov/gcos_wgsp/Timeseries/DMI/>
- Asymmetric and Symmetric SAM indices (ASYMSAM):
  <https://www.cima.fcen.uba.ar/~elio.campitelli/asymsam/>
