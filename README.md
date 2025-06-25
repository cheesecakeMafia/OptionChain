# OptionChain 📊 [ARCHIVED PROJECT]

⚠️ **PROJECT STATUS: NO LONGER ACTIVE** ⚠️

This Python tool was designed for fetching, analyzing, and visualizing option chain data from NSE India (National Stock Exchange of India). However, **NSE India has updated their API endpoints to use dynamic URLs with additional security measures, making this implementation non-functional**.

**This repository is maintained for educational and reference purposes only.**

## 🚫 **Why This Project No Longer Works**

**NSE India API Changes**: The National Stock Exchange of India has implemented significant changes to their API infrastructure:

- **Dynamic Endpoints**: The static API URLs this project relied on have been replaced with dynamic, session-based endpoints
- **Enhanced Security**: Additional authentication mechanisms and anti-bot measures have been implemented
- **Rate Limiting**: Stricter rate limiting and request validation
- **Session Management**: Complex session management requirements that require browser-like behavior

## 🚀 Features (Historical - No Longer Functional)

- **~~Real-time Data Fetching~~**: ❌ **NO LONGER WORKS** - NSE API endpoints deprecated
- **Advanced Analysis**: ✅ Still functional with mock/sample data
- **Professional Visualizations**: ✅ Still functional with sample data
- **Type-Safe**: ✅ Full type hints and static type checking with mypy
- **Well-Tested**: ✅ Comprehensive test suite with pytest
- **Modern Python**: ✅ Built for Python 3.12+ with modern practices

## 📈 Visualizations

### 1. Implied Volatility Skew
Visualize how implied volatility varies across different strike prices for a given expiry.

### 2. Term Structure Analysis 
Analyze how implied volatility changes across different expiry dates for a specific strike.

### 3. Open Interest Distribution
View the distribution of open interest and changes in OI across the option chain.

## 🛠️ Installation

### Using uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/OptionChain.git
cd OptionChain

# Install with uv
uv sync
```

### Using pip
```bash
# Clone the repository
git clone https://github.com/yourusername/OptionChain.git
cd OptionChain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage (Educational Purposes Only)

⚠️ **WARNING**: The data fetching functionality will not work due to NSE API changes. You can still explore the code structure and visualization capabilities with mock data.

### Command Line Interface

```bash
# Run the comprehensive example script (will show errors due to API issues)
uv run python main.py

# Or run the package directly (will show deprecation warnings)
uv run python -m optionchain

# Note: You'll see warnings that NSE API endpoints are deprecated
```

### Python API

```python
from optionchain import OptionChainAnalyzer

# Initialize the analyzer
analyzer = OptionChainAnalyzer()

# Fetch and analyze option chain data
option_chain = analyzer.analyze_symbol("NIFTY", oi_cutoff=100)

# Generate visualizations
analyzer.plot_volatility_skew(expiry_index=0)  # Nearest expiry
analyzer.plot_term_structure()  # ATM strike by default
analyzer.plot_open_interest_analysis()  # OI distribution

# Get summary statistics
summary = analyzer.get_summary()
print(f"ATM Strike: {summary['atm_strike']}")
print(f"Total Call OI: {summary['total_call_oi']:,}")
print(f"Total Put OI: {summary['total_put_oi']:,}")
```

### Advanced Usage

```python
from optionchain import OptionChain, NSEOptionFetcher

# Direct API access
fetcher = NSEOptionFetcher(timeout=30, max_retries=3)
option_chain = fetcher.fetch_option_chain("BANKNIFTY")

# Custom filtering
filtered_chain = option_chain.filter_by_oi(cutoff=500)

# Group by expiry
expiry_groups = option_chain.group_by_expiry()
for expiry_idx, data in expiry_groups.items():
    print(f"Expiry {expiry_idx}: {len(data)} strikes")

# Group by strike
strike_groups = option_chain.group_by_strike()
atm_strike = option_chain.get_atm_strike()
print(f"ATM Strike: {atm_strike}")
```

## 🏗️ Project Structure

```
OptionChain/
├── src/
│   └── optionchain/
│       ├── __init__.py         # Package exports
│       ├── __main__.py         # CLI entry point
│       ├── analysis.py         # Main analyzer class
│       ├── data_fetcher.py     # NSE API integration
│       ├── models.py           # Data models
│       └── visualization.py    # Plotting utilities
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── main.py                     # Example implementation script
├── pyproject.toml              # Project configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🧑‍💻 Development

### Setup Development Environment

```bash
# Clone and install with development dependencies
git clone https://github.com/yourusername/OptionChain.git
cd OptionChain
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_models.py -v
```

### Code Quality

```bash
# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/

# Format code
uv run black src/ tests/
uv run isort src/ tests/
```

### Building Documentation

```bash
# Generate API documentation
uv run pdoc --html --output-dir docs src/optionchain
```

## 📊 Data Structure

The tool works with the following data structure:

```python
@dataclass
class OptionData:
    expiry: datetime
    strike: float
    call_oi: int
    call_coi: int
    call_iv: float
    call_ltp: float
    put_oi: int
    put_coi: int
    put_iv: float
    put_ltp: float

@dataclass
class OptionChain:
    security: str
    underlying_price: float
    data: pd.DataFrame
    expiries: List[datetime]
    strikes: List[float]
```

## 🔧 Configuration

The tool uses sensible defaults but can be customized:

```python
# Custom timeout and retries
fetcher = NSEOptionFetcher(timeout=60, max_retries=5)

# Custom visualization settings
visualizer = OptionChainVisualizer(figsize=(20, 12))

# Analysis with custom OI cutoff
analyzer.analyze_symbol("NIFTY", oi_cutoff=1000)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards

- Use type hints for all functions
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add tests for new features
- Ensure 80%+ test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NSE India for providing the option chain data API
- The Python quantitative finance community
- Contributors and users of this tool

## ⚠️ Disclaimer & Project Status

**IMPORTANT**: This project is **NO LONGER FUNCTIONAL** due to NSE India API changes. The data fetching capabilities do not work and will return errors.

**Educational Use Only**: This repository is maintained solely for educational purposes to demonstrate:
- Modern Python package structure and development practices
- Financial data analysis patterns and methodologies  
- Option chain data modeling and visualization techniques
- Professional software engineering practices in quantitative finance

**No Financial Advice**: This tool was designed for educational and research purposes only. Always verify data accuracy and consult with financial professionals before making investment decisions. The authors are not responsible for any financial losses incurred through the use of this tool.

**API Status**: NSE India has implemented dynamic API endpoints with enhanced security measures that this static implementation cannot access.

## 🚧 ~~Roadmap~~ (Project Archived)

**Note**: Development has been discontinued due to NSE API changes. The following features were planned but will not be implemented:

- ~~Add support for equity options (not just indices)~~ ❌ Cancelled
- ~~Implement options Greeks calculations (Delta, Gamma, Theta, Vega)~~ ❌ Cancelled  
- ~~Add real-time data streaming capabilities~~ ❌ Cancelled (API no longer accessible)
- ~~Create web interface with Streamlit/Dash~~ ❌ Cancelled
- ~~Add portfolio analysis features~~ ❌ Cancelled
- ~~Implement backtesting framework~~ ❌ Cancelled
- ~~Support for international markets~~ ❌ Cancelled

## 📧 Contact

For questions, suggestions, or collaborations, please open an issue on GitHub or contact the maintainers.

---

**Note**: This tool requires a stable internet connection to fetch data from NSE India. Data availability depends on market hours and NSE API status.