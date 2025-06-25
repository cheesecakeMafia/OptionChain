"""Unit tests for analysis module."""

from unittest.mock import patch

from src.optionchain.analysis import OptionChainAnalyzer


class TestOptionChainAnalyzer:
    """Test cases for OptionChainAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        analyzer = OptionChainAnalyzer()

        assert analyzer.fetcher is not None
        assert analyzer.visualizer is not None
        assert analyzer.current_chain is None

    @patch('src.optionchain.analysis.NSEOptionFetcher.fetch_option_chain')
    def test_analyze_symbol_success(self, mock_fetch, sample_option_chain):
        """Test successful symbol analysis."""
        mock_fetch.return_value = sample_option_chain

        analyzer = OptionChainAnalyzer()
        result = analyzer.analyze_symbol("NIFTY")

        assert result is not None
        assert result.security == "NIFTY"
        assert analyzer.current_chain is not None
        mock_fetch.assert_called_once_with("NIFTY")

    @patch('src.optionchain.analysis.NSEOptionFetcher.fetch_option_chain')
    def test_analyze_symbol_failure(self, mock_fetch):
        """Test symbol analysis failure."""
        mock_fetch.return_value = None

        analyzer = OptionChainAnalyzer()
        result = analyzer.analyze_symbol("INVALID")

        assert result is None
        assert analyzer.current_chain is None
        mock_fetch.assert_called_once_with("INVALID")

    def test_get_summary_no_data(self):
        """Test get_summary with no data."""
        analyzer = OptionChainAnalyzer()
        summary = analyzer.get_summary()

        assert summary == {}

    def test_get_summary_with_data(self, sample_option_chain):
        """Test get_summary with data."""
        analyzer = OptionChainAnalyzer()
        analyzer.current_chain = sample_option_chain

        summary = analyzer.get_summary()

        assert summary["security"] == "NIFTY"
        assert summary["underlying_price"] == 21250.0
        assert summary["atm_strike"] == 21000.0
        assert "total_records" in summary
        assert "total_call_oi" in summary
        assert "total_put_oi" in summary

    def test_plot_methods_no_data(self, capsys):
        """Test plotting methods with no data."""
        analyzer = OptionChainAnalyzer()

        # These should log errors and return without plotting
        analyzer.plot_volatility_skew()
        analyzer.plot_term_structure()
        analyzer.plot_open_interest_analysis()

        # Should not raise exceptions
