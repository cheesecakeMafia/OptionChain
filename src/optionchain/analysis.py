"""Main analysis module for option chain processing."""

from __future__ import annotations

import logging
from typing import Any

from .data_fetcher import NSEOptionFetcher
from .models import OptionChain
from .visualization import OptionChainVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OptionChainAnalyzer:
    """Main class for option chain analysis and visualization."""

    def __init__(self) -> None:
        """Initialize the analyzer with data fetcher and visualizer."""
        self.fetcher = NSEOptionFetcher()
        self.visualizer = OptionChainVisualizer()
        self.current_chain: OptionChain | None = None

    def analyze_symbol(self, symbol: str, oi_cutoff: int = 100) -> OptionChain | None:
        """Analyze option chain for a given symbol.

        Args:
            symbol: NSE symbol to analyze
            oi_cutoff: Minimum open interest filter

        Returns:
            OptionChain object if successful, None otherwise
        """
        logger.info(f"Fetching option chain data for {symbol}")

        option_chain = self.fetcher.fetch_option_chain(symbol)
        if not option_chain:
            logger.error(f"Failed to fetch data for {symbol}")
            return None

        logger.info(f"Successfully fetched data for {symbol}")
        logger.info(f"Underlying price: {option_chain.underlying_price:.2f}")
        logger.info(f"ATM strike: {option_chain.get_atm_strike():.2f}")
        logger.info(f"Available expiries: {len(option_chain.expiries)}")
        logger.info(f"Available strikes: {len(option_chain.strikes)}")

        # Apply OI filter
        filtered_chain = option_chain.filter_by_oi(oi_cutoff)
        logger.info(
            f"After OI filter ({oi_cutoff}): {len(filtered_chain.data)} records"
        )

        self.current_chain = filtered_chain
        return filtered_chain

    def plot_volatility_skew(self, expiry_index: int = 0) -> None:
        """Plot volatility skew for the current option chain.

        Args:
            expiry_index: Index of expiry to plot (default: nearest expiry)
        """
        if not self.current_chain:
            logger.error("No option chain data available. Run analyze_symbol() first.")
            return

        expiry_data = self.current_chain.group_by_expiry()
        self.visualizer.plot_volatility_skew(
            expiry_data=expiry_data,
            expiry_index=expiry_index,
            underlying_price=self.current_chain.underlying_price,
            title=f"{self.current_chain.security} - Volatility Skew",
        )

    def plot_term_structure(self, strike: float | None = None) -> None:
        """Plot term structure for the current option chain.

        Args:
            strike: Strike price to plot (default: ATM strike)
        """
        if not self.current_chain:
            logger.error("No option chain data available. Run analyze_symbol() first.")
            return

        if strike is None:
            strike = self.current_chain.get_atm_strike()

        strike_data = self.current_chain.group_by_strike()

        # Add Expiry column back to strike data for plotting
        for s, df in strike_data.items():
            if s == strike:
                # Get expiry info from original data
                expiry_info = self.current_chain.data[
                    self.current_chain.data["Strike"] == s
                ]["Expiry"].values
                df["Expiry"] = expiry_info[: len(df)]
                break

        self.visualizer.plot_term_structure(
            strike_data=strike_data,
            strike=strike,
            title=f"{self.current_chain.security} - Term Structure (Strike: {strike})",
        )

    def plot_open_interest_analysis(self, expiry_index: int = 0) -> None:
        """Plot open interest analysis for the current option chain.

        Args:
            expiry_index: Index of expiry to analyze (default: nearest expiry)
        """
        if not self.current_chain:
            logger.error("No option chain data available. Run analyze_symbol() first.")
            return

        self.visualizer.plot_open_interest_analysis(
            option_chain=self.current_chain, expiry_index=expiry_index
        )

    def get_summary(self) -> dict[str, Any]:
        """Get summary statistics for the current option chain.

        Returns:
            Dictionary containing summary statistics
        """
        if not self.current_chain:
            return {}

        data = self.current_chain.data

        return {
            "security": self.current_chain.security,
            "underlying_price": self.current_chain.underlying_price,
            "atm_strike": self.current_chain.get_atm_strike(),
            "total_records": len(data),
            "expiries_count": len(self.current_chain.expiries),
            "strikes_count": len(self.current_chain.strikes),
            "total_call_oi": data["Call OI"].sum(),
            "total_put_oi": data["Put OI"].sum(),
            "max_call_oi_strike": data.loc[data["Call OI"].idxmax(), "Strike"],
            "max_put_oi_strike": data.loc[data["Put OI"].idxmax(), "Strike"],
        }


def main() -> None:
    """Main function for command-line usage."""
    try:
        # Get user input
        security = (
            input("For what security do you want an option chain? ").strip().upper()
        )

        if not security:
            print("Please provide a valid security symbol.")
            return

        # Initialize analyzer
        analyzer = OptionChainAnalyzer()

        # Analyze the symbol
        option_chain = analyzer.analyze_symbol(security)

        if not option_chain:
            print(f"Failed to fetch option chain data for {security}")
            return

        # Display summary
        summary = analyzer.get_summary()
        print("\n" + "=" * 50)
        print("OPTION CHAIN SUMMARY")
        print("=" * 50)
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("=" * 50)

        # Create visualizations
        print("\nGenerating visualizations...")
        analyzer.plot_volatility_skew(expiry_index=0)
        analyzer.plot_term_structure()
        analyzer.plot_open_interest_analysis(expiry_index=0)

        # Display first few rows of data
        print("\nFirst 10 rows of option chain data:")
        print(option_chain.data.head(10))

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
