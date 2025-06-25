# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based option chain analysis tool that scrapes NSE India's option chain data and performs quantitative analysis including skew plots and term structure visualization. The project uses uv for package management and is structured as a quantitative finance analysis toolkit.

## Architecture

- **OptionChainAnalysis.py**: Core module containing the main analysis logic, data scraping from NSE India API, and plotting functions
- **main.py**: Entry point module (currently minimal placeholder)
- **OptionChain.ipynb**: Jupyter notebook for interactive analysis
- Uses pandas DataFrames for option chain data manipulation
- Matplotlib and cufflinks for visualization
- Requests library with session management for NSE India API scraping

## Common Commands

### Package Management
```bash
# Install dependencies
uv install

# Run in project environment
uv run python OptionChainAnalysis.py
uv run python main.py

# Add new dependencies
uv add <package-name>
```

### Testing
```bash
# Run tests (pytest is included in dependencies)
uv run pytest

# Run specific test
uv run pytest tests/test_specific.py
```

### Development
```bash
# Run Jupyter notebook
uv run jupyter notebook OptionChain.ipynb

# Run the main analysis script
uv run python OptionChainAnalysis.py
```

## Key Functions and Data Flow

1. **Data Acquisition**: NSE India API scraping with proper headers and session management
2. **Data Processing**: `option_dataframe()` converts nested JSON to structured DataFrame
3. **Data Organization**: 
   - `by_expiry()` - organizes data by expiration dates
   - `by_strike()` - organizes data by strike prices
4. **Analysis Functions**:
   - `strike_ATM()` - finds at-the-money strike price
   - `plot_graph_expiry()` - plots volatility skew for given expiry
   - `plot_graph_strike()` - plots term structure for given strike

## Data Structure

The main data structure is a pandas DataFrame with columns:
- Expiry, Call OI, Call C_OI, Call IV, Call LTP, Strike, Put LTP, Put IV, Put C_OI, Put OI

Data is organized into dictionaries:
- `expiry_df`: keyed by expiry index
- `strike_df`: keyed by strike price

## Dependencies

Core dependencies (see pyproject.toml):
- pandas: data manipulation
- requests: API calls
- matplotlib: plotting
- cufflinks: enhanced plotting
- scipy: scientific computing
- pytest: testing framework