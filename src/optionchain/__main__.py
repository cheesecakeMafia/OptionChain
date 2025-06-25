"""Command line interface for OptionChain analysis."""

import sys
from pathlib import Path

# Add project root to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from optionchain.analysis import main

if __name__ == "__main__":
    main()
