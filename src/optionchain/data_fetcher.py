"""Data fetching utilities for NSE India option chains."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import OptionChain

logger = logging.getLogger(__name__)


class NSEOptionFetcher:
    """Fetches option chain data from NSE India.

    WARNING: This implementation is no longer functional as NSE India has
    updated their API endpoints to use dynamic URLs with additional security
    measures. The static BASE_URL approach no longer works.

    This class is maintained for educational and reference purposes only.
    """

    # DEPRECATED: This URL no longer works due to NSE API changes
    BASE_URL = "https://www.nseindia.com/api/option-chain-indices"

    def __init__(self, timeout: int = 30, max_retries: int = 3) -> None:
        """Initialize the NSE option fetcher.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set headers to mimic browser request
        session.headers.update(
            {
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/97.0.4692.99 Safari/537.36"
                ),
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
            }
        )

        return session

    def fetch_option_chain(self, symbol: str) -> OptionChain | None:
        """Fetch option chain data for a given symbol.

        WARNING: This method is no longer functional due to NSE API changes.
        NSE India has implemented dynamic API endpoints that require additional
        authentication and session management that this implementation does not support.

        Args:
            symbol: NSE symbol (e.g., 'NIFTY', 'BANKNIFTY')

        Returns:
            None (always fails due to deprecated API endpoint)
        """
        symbol = symbol.upper()
        url = f"{self.BASE_URL}?symbol={symbol}"

        logger.warning(
            f"NSE API endpoint is deprecated. Cannot fetch data for {symbol}. "
            "NSE India has updated their API to use dynamic endpoints that require "
            "additional authentication measures not supported by this implementation."
        )

        try:
            # Initial request to get cookies
            initial_response = self.session.get(url, timeout=self.timeout)
            initial_response.raise_for_status()

            # Main request with cookies
            response = self.session.get(
                url, cookies=dict(initial_response.cookies), timeout=self.timeout
            )
            response.raise_for_status()

            # Check if response is JSON
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                logger.error(
                    f"NSE API returned non-JSON response for {symbol}. Content-Type: {content_type}"
                )
                return None

            data = response.json()
            return self._parse_response_data(data, symbol)

        except requests.RequestException as e:
            logger.error(f"Failed to fetch option chain for {symbol}: {e}")
            logger.error(
                "This is expected as NSE has deprecated the static API endpoint."
            )
            return None
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to parse response data for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {symbol}: {e}")
            return None

    def _parse_response_data(self, data: dict[str, Any], symbol: str) -> OptionChain:
        """Parse NSE API response into OptionChain object.

        Args:
            data: Raw API response data
            symbol: NSE symbol

        Returns:
            OptionChain object

        Raises:
            KeyError: If required data fields are missing
            ValueError: If data is invalid
        """
        records = data["records"]["data"]
        df = pd.DataFrame(records).fillna(0)

        # Parse option data
        option_data = []
        underlying_price = 0.0

        for _, row in df.iterrows():
            strike = row.iloc[0]
            expiry = pd.to_datetime(row.iloc[1])

            # Extract call data
            call_data = row.iloc[-1] if row.iloc[-1] != 0 else {}
            call_oi = call_data.get("openInterest", 0)
            call_coi = call_data.get("changeinOpenInterest", 0)
            call_ltp = call_data.get("lastPrice", 0.0)
            call_iv = call_data.get("impliedVolatility", 0.0)

            # Extract put data
            put_data = row.iloc[-2] if row.iloc[-2] != 0 else {}
            put_oi = put_data.get("openInterest", 0)
            put_coi = put_data.get("changeinOpenInterest", 0)
            put_ltp = put_data.get("lastPrice", 0.0)
            put_iv = put_data.get("impliedVolatility", 0.0)

            # Get underlying price from first valid entry
            if underlying_price == 0.0 and put_data:
                underlying_price = put_data.get("underlyingValue", 0.0)

            option_entry = {
                "Expiry": expiry,
                "Call OI": call_oi,
                "Call C_OI": call_coi,
                "Call IV": call_iv,
                "Call LTP": call_ltp,
                "Strike": strike,
                "Put LTP": put_ltp,
                "Put IV": put_iv,
                "Put C_OI": put_coi,
                "Put OI": put_oi,
            }
            option_data.append(option_entry)

        option_df = pd.DataFrame(option_data)
        expiries = sorted(option_df["Expiry"].unique())
        strikes = sorted(option_df["Strike"].unique())

        return OptionChain(
            security=symbol,
            underlying_price=underlying_price,
            data=option_df,
            expiries=expiries,
            strikes=strikes,
        )


# NOTE: Test code removed as NSE API is no longer functional with this implementation
