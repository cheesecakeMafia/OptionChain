"""Visualization utilities for option chain analysis."""

from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import pandas as pd

from .models import OptionChain

logger = logging.getLogger(__name__)


class OptionChainVisualizer:
    """Creates visualizations for option chain data."""

    def __init__(self, figsize: tuple[int, int] = (16, 9)) -> None:
        """Initialize the visualizer.

        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
        plt.style.use("default")

    def plot_volatility_skew(
        self,
        expiry_data: dict[int, pd.DataFrame],
        expiry_index: int = 0,
        underlying_price: float | None = None,
        title: str | None = None,
    ) -> None:
        """Plot implied volatility skew for a specific expiry.

        Args:
            expiry_data: Dictionary of DataFrames grouped by expiry
            expiry_index: Index of expiry to plot
            underlying_price: Current underlying price for reference line
            title: Custom title for the plot
        """
        if expiry_index not in expiry_data:
            logger.error(f"Expiry index {expiry_index} not found in data")
            return

        data = expiry_data[expiry_index].copy()

        # Filter out zero IV values
        data = data[(data["Call IV"] > 0) & (data["Put IV"] > 0)]

        if data.empty:
            logger.warning(f"No valid IV data for expiry index {expiry_index}")
            return

        plt.figure(figsize=self.figsize)

        # Plot call and put IV
        plt.plot(data["Strike"], data["Call IV"], "b-", linewidth=2, label="Call IV")
        plt.plot(data["Strike"], data["Put IV"], "r-", linewidth=2, label="Put IV")

        # Add underlying price reference line
        if underlying_price:
            plt.axvline(
                x=underlying_price,
                color="green",
                linestyle="--",
                alpha=0.7,
                label=f"Underlying: {underlying_price:.2f}"
            )

        plt.grid(True, alpha=0.3)
        plt.title(title or "Implied Volatility Skew")
        plt.xlabel("Strike Price")
        plt.ylabel("Implied Volatility (%)")
        plt.legend()
        plt.ylim(bottom=0)

        # Improve layout
        plt.tight_layout()
        plt.show()

    def plot_term_structure(
        self,
        strike_data: dict[float, pd.DataFrame],
        strike: float,
        title: str | None = None,
    ) -> None:
        """Plot implied volatility term structure for a specific strike.

        Args:
            strike_data: Dictionary of DataFrames grouped by strike
            strike: Strike price to plot
            title: Custom title for the plot
        """
        if strike not in strike_data:
            logger.error(f"Strike {strike} not found in data")
            return

        data = strike_data[strike].copy()

        # Ensure Expiry column exists and convert to datetime
        if "Expiry" not in data.columns:
            logger.error("Expiry column not found in strike data")
            return

        data["Expiry"] = pd.to_datetime(data["Expiry"])

        # Filter out zero IV values
        data = data[(data["Call IV"] > 0) & (data["Put IV"] > 0)]

        if data.empty:
            logger.warning(f"No valid IV data for strike {strike}")
            return

        # Sort by expiry
        data = data.sort_values("Expiry")

        plt.figure(figsize=self.figsize)

        # Plot call and put term structure
        plt.plot(
            data["Expiry"],
            data["Call IV"],
            "b-o",
            linewidth=2,
            markersize=6,
            label="Call Term Structure"
        )
        plt.plot(
            data["Expiry"],
            data["Put IV"],
            "r-o",
            linewidth=2,
            markersize=6,
            label="Put Term Structure"
        )

        plt.grid(True, alpha=0.3)
        plt.title(title or f"IV Term Structure - Strike {strike}")
        plt.xlabel("Expiry Date")
        plt.ylabel("Implied Volatility (%)")
        plt.legend()
        plt.ylim(bottom=0)

        # Improve x-axis formatting
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_open_interest_analysis(
        self,
        option_chain: OptionChain,
        expiry_index: int = 0,
    ) -> None:
        """Plot open interest analysis for calls and puts.

        Args:
            option_chain: OptionChain object
            expiry_index: Index of expiry to analyze
        """
        expiry_data = option_chain.group_by_expiry()

        if expiry_index not in expiry_data:
            logger.error(f"Expiry index {expiry_index} not found")
            return

        data = expiry_data[expiry_index]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize)

        # Plot OI
        ax1.bar(data["Strike"], data["Call OI"], alpha=0.7, color="blue", label="Call OI")
        ax1.bar(data["Strike"], -data["Put OI"], alpha=0.7, color="red", label="Put OI")
        ax1.axvline(x=option_chain.underlying_price, color="green", linestyle="--", alpha=0.7)
        ax1.set_title("Open Interest Distribution")
        ax1.set_ylabel("Open Interest")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot Change in OI
        ax2.bar(data["Strike"], data["Call C_OI"], alpha=0.7, color="lightblue", label="Call ΔOI")
        ax2.bar(data["Strike"], -data["Put C_OI"], alpha=0.7, color="lightcoral", label="Put ΔOI")
        ax2.axvline(x=option_chain.underlying_price, color="green", linestyle="--", alpha=0.7)
        ax2.axhline(y=0, color="black", linestyle="-", alpha=0.5)
        ax2.set_title("Change in Open Interest")
        ax2.set_xlabel("Strike Price")
        ax2.set_ylabel("Change in OI")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
