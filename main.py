#!/usr/bin/env python3
"""
OptionChain Example Implementation

This script demonstrates how to use the OptionChain package to analyze
NSE India option chain data. It shows various usage patterns and features
of the library.

Usage:
    python main.py
    
    or
    
    uv run python main.py
"""

import logging
from typing import Optional

from src.optionchain import OptionChainAnalyzer


def setup_logging() -> None:
    """Configure logging for the example."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )


def interactive_analysis() -> None:
    """Run interactive analysis with user input."""
    print("🔍 OptionChain Interactive Analysis")
    print("=" * 40)
    
    # Get user input for security
    while True:
        security = input("\nEnter NSE symbol (e.g., NIFTY, BANKNIFTY): ").strip().upper()
        if security:
            break
        print("❌ Please enter a valid symbol.")
    
    # Get OI cutoff preference
    try:
        oi_cutoff = input(f"Enter minimum Open Interest cutoff (default: 100): ").strip()
        oi_cutoff = int(oi_cutoff) if oi_cutoff else 100
    except ValueError:
        oi_cutoff = 100
        print(f"⚠️  Using default OI cutoff: {oi_cutoff}")
    
    # Initialize analyzer and fetch data
    print(f"\n📊 Analyzing {security} with OI cutoff: {oi_cutoff}")
    analyzer = OptionChainAnalyzer()
    
    try:
        option_chain = analyzer.analyze_symbol(security, oi_cutoff=oi_cutoff)
        
        if not option_chain:
            print(f"❌ Failed to fetch data for {security}")
            return
        
        # Display summary
        display_summary(analyzer)
        
        # Ask user what visualizations they want
        show_visualizations(analyzer)
        
        # Optionally show raw data
        if input("\nShow first 10 rows of data? (y/N): ").lower().startswith('y'):
            print("\n📋 Option Chain Data (First 10 rows):")
            print(option_chain.data.head(10).to_string(index=False))
    
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        logging.error(f"Analysis failed: {e}")


def display_summary(analyzer: OptionChainAnalyzer) -> None:
    """Display summary statistics."""
    summary = analyzer.get_summary()
    
    print("\n" + "=" * 50)
    print("📈 OPTION CHAIN SUMMARY")
    print("=" * 50)
    
    for key, value in summary.items():
        if isinstance(value, (int, float)) and key.endswith('oi'):
            # Format large numbers with commas
            print(f"{key.replace('_', ' ').title():.<30} {value:,}")
        elif isinstance(value, float):
            print(f"{key.replace('_', ' ').title():.<30} {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title():.<30} {value}")
    
    print("=" * 50)


def show_visualizations(analyzer: OptionChainAnalyzer) -> None:
    """Show various visualizations based on user preference."""
    print("\n🎨 Available Visualizations:")
    print("1. Implied Volatility Skew")
    print("2. Term Structure Analysis")
    print("3. Open Interest Distribution")
    print("4. All visualizations")
    print("5. Skip visualizations")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        print("📊 Generating Volatility Skew...")
        analyzer.plot_volatility_skew()
    elif choice == "2":
        print("📊 Generating Term Structure...")
        analyzer.plot_term_structure()
    elif choice == "3":
        print("📊 Generating Open Interest Analysis...")
        analyzer.plot_open_interest_analysis()
    elif choice == "4":
        print("📊 Generating all visualizations...")
        analyzer.plot_volatility_skew()
        analyzer.plot_term_structure()
        analyzer.plot_open_interest_analysis()
    else:
        print("⏭️  Skipping visualizations")


def programmatic_example() -> None:
    """Example of programmatic usage without user interaction."""
    print("\n🤖 Programmatic Analysis Example")
    print("=" * 40)
    
    # Example with NIFTY
    analyzer = OptionChainAnalyzer()
    
    print("📊 Fetching NIFTY option chain...")
    option_chain = analyzer.analyze_symbol("NIFTY", oi_cutoff=500)
    
    if option_chain:
        # Get summary
        summary = analyzer.get_summary()
        print(f"✅ Successfully analyzed NIFTY")
        print(f"   Underlying Price: ₹{summary['underlying_price']:.2f}")
        print(f"   ATM Strike: ₹{summary['atm_strike']:.2f}")
        print(f"   Total Call OI: {summary['total_call_oi']:,}")
        print(f"   Total Put OI: {summary['total_put_oi']:,}")
        
        # Example of custom analysis
        print("\n🔍 Custom Analysis:")
        
        # Find strikes with highest OI
        data = option_chain.data
        max_call_oi_strike = data.loc[data['Call OI'].idxmax(), 'Strike']
        max_put_oi_strike = data.loc[data['Put OI'].idxmax(), 'Strike']
        
        print(f"   Highest Call OI: ₹{max_call_oi_strike:.0f}")
        print(f"   Highest Put OI: ₹{max_put_oi_strike:.0f}")
        
        # Calculate Put-Call ratio
        total_call_oi = summary['total_call_oi']
        total_put_oi = summary['total_put_oi']
        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
        print(f"   Put-Call Ratio: {pcr:.2f}")
        
        # Market sentiment based on PCR
        if pcr > 1.2:
            sentiment = "🐻 Bearish"
        elif pcr < 0.8:
            sentiment = "🐂 Bullish"
        else:
            sentiment = "🦆 Neutral"
        print(f"   Market Sentiment: {sentiment}")
    
    else:
        print("❌ Failed to fetch NIFTY data")


def advanced_example() -> None:
    """Advanced usage examples."""
    print("\n🚀 Advanced Usage Examples")
    print("=" * 40)
    
    from src.optionchain.data_fetcher import NSEOptionFetcher
    from src.optionchain.visualization import OptionChainVisualizer
    
    # Custom fetcher with longer timeout
    print("🔧 Using custom data fetcher...")
    fetcher = NSEOptionFetcher(timeout=60, max_retries=5)
    option_chain = fetcher.fetch_option_chain("BANKNIFTY")
    
    if option_chain:
        print(f"✅ Fetched BANKNIFTY data: {len(option_chain.data)} records")
        
        # Custom filtering
        high_oi_chain = option_chain.filter_by_oi(cutoff=1000)
        print(f"🔍 After high OI filter: {len(high_oi_chain.data)} records")
        
        # Group analysis
        expiry_groups = option_chain.group_by_expiry(cutoff=500)
        print(f"📅 Available expiries: {len(expiry_groups)}")
        
        for i, (expiry_idx, data) in enumerate(expiry_groups.items()):
            if i < 3:  # Show first 3 expiries
                print(f"   Expiry {expiry_idx}: {len(data)} strikes")
        
        # Custom visualization
        visualizer = OptionChainVisualizer(figsize=(20, 12))
        print("🎨 Creating custom visualization (if requested)...")
        
        if input("Generate custom volatility skew? (y/N): ").lower().startswith('y'):
            visualizer.plot_volatility_skew(
                expiry_data=expiry_groups,
                expiry_index=0,
                underlying_price=option_chain.underlying_price,
                title="BANKNIFTY Custom Volatility Skew"
            )


def main() -> None:
    """Main function with example menu."""
    setup_logging()
    
    print("🔗 OptionChain Analysis Tool")
    print("NSE India Option Chain Data Analysis")
    print("=" * 40)
    
    while True:
        print("\n📋 Select an example:")
        print("1. Interactive Analysis (recommended)")
        print("2. Programmatic Example")
        print("3. Advanced Usage Examples")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        try:
            if choice == "1":
                interactive_analysis()
            elif choice == "2":
                programmatic_example()
            elif choice == "3":
                advanced_example()
            elif choice == "4":
                print("👋 Thank you for using OptionChain!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
                continue
            
            # Ask if user wants to continue
            if input("\nRun another example? (Y/n): ").lower().startswith('n'):
                print("👋 Thank you for using OptionChain!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            logging.error(f"Unexpected error: {e}")
            
            if input("Continue with other examples? (Y/n): ").lower().startswith('n'):
                break


if __name__ == "__main__":
    main()
