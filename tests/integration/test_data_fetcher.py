"""Integration tests for data fetcher."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.optionchain.data_fetcher import NSEOptionFetcher


class TestNSEOptionFetcher:
    """Integration tests for NSE data fetching."""

    def test_fetcher_initialization(self):
        """Test fetcher initialization."""
        fetcher = NSEOptionFetcher()

        assert fetcher.timeout == 30
        assert fetcher.session is not None
        assert "Mozilla" in fetcher.session.headers["user-agent"]

    def test_fetcher_custom_params(self):
        """Test fetcher with custom parameters."""
        fetcher = NSEOptionFetcher(timeout=60, max_retries=5)

        assert fetcher.timeout == 60

    @patch('requests.Session.get')
    def test_fetch_option_chain_success(self, mock_get, mock_nse_response):
        """Test successful option chain fetch."""
        # Mock the requests
        mock_response = Mock()
        mock_response.json.return_value = mock_nse_response
        mock_response.raise_for_status.return_value = None
        mock_response.cookies = {}
        mock_get.return_value = mock_response

        fetcher = NSEOptionFetcher()
        result = fetcher.fetch_option_chain("NIFTY")

        assert result is not None
        assert result.security == "NIFTY"
        assert mock_get.call_count == 2  # Initial + main request

    @patch('requests.Session.get')
    def test_fetch_option_chain_request_failure(self, mock_get):
        """Test option chain fetch with request failure."""
        mock_get.side_effect = requests.RequestException("Network error")

        fetcher = NSEOptionFetcher()
        result = fetcher.fetch_option_chain("NIFTY")

        assert result is None

    @patch('requests.Session.get')
    def test_fetch_option_chain_invalid_response(self, mock_get):
        """Test option chain fetch with invalid response."""
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "data"}
        mock_response.raise_for_status.return_value = None
        mock_response.cookies = {}
        mock_get.return_value = mock_response

        fetcher = NSEOptionFetcher()
        result = fetcher.fetch_option_chain("NIFTY")

        assert result is None

    @pytest.mark.slow
    def test_session_retry_strategy(self):
        """Test that session has retry strategy configured."""
        fetcher = NSEOptionFetcher(max_retries=2)

        # Check that adapter is configured
        adapter = fetcher.session.get_adapter("https://example.com")
        assert adapter is not None
