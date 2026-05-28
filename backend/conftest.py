"""pytest configuration for backend tests."""
import sys
from pathlib import Path

# Add parent directory to Python path so connectors can be imported
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
