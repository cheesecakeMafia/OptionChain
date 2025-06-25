"""Data models for option chain analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class OptionData:
    """Individual option data point."""

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
    """Complete option chain data."""

    security: str
    underlying_price: float
    data: pd.DataFrame
    expiries: list[datetime]
    strikes: list[float]

    def __post_init__(self) -> None:
        """Validate and process option chain data."""
        if self.data.empty:
            raise ValueError("Option chain data cannot be empty")

        # Ensure expiries are datetime objects
        self.expiries = sorted([
            pd.to_datetime(exp) if not isinstance(exp, datetime) else exp
            for exp in self.expiries
        ])

        # Ensure strikes are sorted
        self.strikes = sorted(self.strikes)

    def get_atm_strike(self) -> float:
        """Find the at-the-money strike price."""
        differences = [abs(self.underlying_price - strike) for strike in self.strikes]
        min_diff_idx = differences.index(min(differences))
        return self.strikes[min_diff_idx]

    def filter_by_oi(self, cutoff: int = 50) -> OptionChain:
        """Filter option chain by minimum open interest."""
        filtered_data = self.data[
            (self.data["Call OI"] > cutoff) | (self.data["Put OI"] > cutoff)
        ].copy()

        return OptionChain(
            security=self.security,
            underlying_price=self.underlying_price,
            data=filtered_data,
            expiries=self.expiries,
            strikes=self.strikes
        )

    def group_by_expiry(self, cutoff: int = 50) -> dict[int, pd.DataFrame]:
        """Group option data by expiry dates."""
        filtered_chain = self.filter_by_oi(cutoff)
        expiry_dict = {}

        for i, expiry in enumerate(self.expiries):
            expiry_data = filtered_chain.data[
                filtered_chain.data["Expiry"] == expiry
            ].copy()
            expiry_data.drop(columns=["Expiry"], inplace=True)
            expiry_data.reset_index(drop=True, inplace=True)
            expiry_dict[i] = expiry_data

        return expiry_dict

    def group_by_strike(self, cutoff: int = 50) -> dict[float, pd.DataFrame]:
        """Group option data by strike prices."""
        filtered_chain = self.filter_by_oi(cutoff)
        strike_dict = {}

        for strike in self.strikes:
            strike_data = filtered_chain.data[
                filtered_chain.data["Strike"] == strike
            ].copy()

            # Remove rows with zero LTP
            strike_data = strike_data[
                (strike_data["Call LTP"] > 0) & (strike_data["Put LTP"] > 0)
            ].copy()

            if not strike_data.empty:
                strike_data.drop(columns=["Strike"], inplace=True)
                strike_data.reset_index(drop=True, inplace=True)
                strike_dict[strike] = strike_data

        return strike_dict
