# Fix TA-Lib Installation Guide

## Option 1: Install precompiled wheel (Recommended)
pip install TA-Lib-0.4.28-cp312-cp312-win_amd64.whl

## Option 2: Install from conda-forge
conda install -c conda-forge ta-lib

## Option 3: Install via pip (may require Visual Studio Build Tools)
pip install TA-Lib

## Verify installation
python -c "import talib; print('TA-Lib installed successfully')"
