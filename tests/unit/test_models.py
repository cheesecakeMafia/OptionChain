"""Unit tests for option chain models."""

from datetime import datetime

import pandas as pd
import pytest

from src.optionchain.models import OptionChain, OptionData


class TestOptionData:
    """Test cases for OptionData dataclass."""

    def test_option_data_creation(self):
        """Test creating an OptionData instance."""
        option_data = OptionData(
            expiry=datetime(2024, 1, 25),
            strike=21000.0,
            call_oi=1000,
            call_coi=100,
            call_iv=15.5,
            call_ltp=250.0,
            put_oi=2000,
            put_coi=-50,
            put_iv=16.0,
            put_ltp=180.0,
        )

        assert option_data.strike == 21000.0
        assert option_data.call_oi == 1000
        assert option_data.put_iv == 16.0


class TestOptionChain:
    """Test cases for OptionChain class."""

    def test_option_chain_creation(self, sample_option_chain):
        """Test creating an OptionChain instance."""
        assert sample_option_chain.security == "NIFTY"
        assert sample_option_chain.underlying_price == 21250.0
        assert len(sample_option_chain.expiries) == 2
        assert len(sample_option_chain.strikes) == 2

    def test_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        with pytest.raises(ValueError, match="Option chain data cannot be empty"):
            OptionChain(
                security="TEST",
                underlying_price=100.0,
                data=pd.DataFrame(),
                expiries=[],
                strikes=[],
            )

    def test_get_atm_strike(self, sample_option_chain):
        """Test ATM strike calculation."""
        atm_strike = sample_option_chain.get_atm_strike()
        # Underlying is 21250, so ATM should be 21000 (closer than 21500)
        assert atm_strike == 21000.0

    def test_filter_by_oi(self, sample_option_chain):
        """Test filtering by open interest."""
        # All sample data has OI > 50, so should return all records
        filtered = sample_option_chain.filter_by_oi(cutoff=50)
        assert len(filtered.data) == 3

        # Higher cutoff should filter some records
        filtered_high = sample_option_chain.filter_by_oi(cutoff=1500)
        assert len(filtered_high.data) < 3

    def test_group_by_expiry(self, sample_option_chain):
        """Test grouping data by expiry."""
        expiry_groups = sample_option_chain.group_by_expiry(cutoff=0)

        # Should have 2 expiry groups
        assert len(expiry_groups) == 2
        assert 0 in expiry_groups
        assert 1 in expiry_groups

        # Check that Expiry column is dropped
        for group_df in expiry_groups.values():
            assert "Expiry" not in group_df.columns

    def test_group_by_strike(self, sample_option_chain):
        """Test grouping data by strike."""
        strike_groups = sample_option_chain.group_by_strike(cutoff=0)

        # Should have entries for strikes that have non-zero LTP
        assert len(strike_groups) >= 1

        # Check that Strike column is dropped
        for group_df in strike_groups.values():
            assert "Strike" not in group_df.columns

    def test_expiries_sorted(self):
        """Test that expiries are automatically sorted."""
        later_date = datetime(2024, 2, 29)
        earlier_date = datetime(2024, 1, 25)

        # Pass dates in reverse order
        chain = OptionChain(
            security="TEST",
            underlying_price=100.0,
            data=pd.DataFrame([{"test": 1}]),
            expiries=[later_date, earlier_date],
            strikes=[100.0],
        )

        # Should be sorted with earlier date first
        assert chain.expiries[0] == earlier_date
        assert chain.expiries[1] == later_date

    def test_strikes_sorted(self):
        """Test that strikes are automatically sorted."""
        chain = OptionChain(
            security="TEST",
            underlying_price=100.0,
            data=pd.DataFrame([{"test": 1}]),
            expiries=[datetime(2024, 1, 25)],
            strikes=[110.0, 90.0, 100.0],
        )

        # Should be sorted in ascending order
        assert chain.strikes == [90.0, 100.0, 110.0]
