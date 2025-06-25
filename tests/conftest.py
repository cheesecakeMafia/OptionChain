"""Pytest configuration and fixtures."""

from datetime import datetime

import pandas as pd
import pytest

from src.optionchain.models import OptionChain


@pytest.fixture
def sample_option_data() -> pd.DataFrame:
    """Create sample option chain data for testing."""
    data = [
        {
            "Expiry": datetime(2024, 1, 25),
            "Strike": 21000.0,
            "Call OI": 1000,
            "Call C_OI": 100,
            "Call IV": 15.5,
            "Call LTP": 250.0,
            "Put OI": 2000,
            "Put C_OI": -50,
            "Put IV": 16.0,
            "Put LTP": 180.0,
        },
        {
            "Expiry": datetime(2024, 1, 25),
            "Strike": 21500.0,
            "Call OI": 1500,
            "Call C_OI": 200,
            "Call IV": 14.0,
            "Call LTP": 150.0,
            "Put OI": 1800,
            "Put C_OI": 0,
            "Put IV": 14.5,
            "Put LTP": 280.0,
        },
        {
            "Expiry": datetime(2024, 2, 29),
            "Strike": 21000.0,
            "Call OI": 800,
            "Call C_OI": 50,
            "Call IV": 16.0,
            "Call LTP": 300.0,
            "Put OI": 1200,
            "Put C_OI": 25,
            "Put IV": 16.5,
            "Put LTP": 200.0,
        },
    ]
    return pd.DataFrame(data)


@pytest.fixture
def sample_option_chain(sample_option_data: pd.DataFrame) -> OptionChain:
    """Create a sample OptionChain object for testing."""
    return OptionChain(
        security="NIFTY",
        underlying_price=21250.0,
        data=sample_option_data,
        expiries=[datetime(2024, 1, 25), datetime(2024, 2, 29)],
        strikes=[21000.0, 21500.0],
    )


@pytest.fixture
def mock_nse_response() -> dict:
    """Mock NSE API response for testing."""
    return {
        "records": {
            "data": [
                {
                    "strikePrice": 21000.0,
                    "expiryDate": "25-Jan-2024",
                    "CE": {
                        "openInterest": 1000,
                        "changeinOpenInterest": 100,
                        "lastPrice": 250.0,
                        "impliedVolatility": 15.5,
                        "underlyingValue": 21250.0,
                    },
                    "PE": {
                        "openInterest": 2000,
                        "changeinOpenInterest": -50,
                        "lastPrice": 180.0,
                        "impliedVolatility": 16.0,
                        "underlyingValue": 21250.0,
                    },
                },
            ]
        }
    }
