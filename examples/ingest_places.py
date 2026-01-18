"""Example script for ingesting places data."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import PlaceIngestor
from data_ingestion.storage import DataExporter


def main():
    """Main function to ingest places data."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Initialize TAT API client
    # Set TAT_API_KEY environment variable or pass it directly
    client = TATAPIClient()
    
    # Initialize place ingestor
    ingestor = PlaceIngestor(client)
    
    # Fetch places data
    print("Fetching places data from TAT API...")
    places = ingestor.fetch_places(
        province=None,  # Fetch all provinces
        category=None,  # Fetch all categories
        max_pages=5     # Limit to 5 pages for example (remove for all data)
    )
    
    print(f"Fetched {len(places)} places")
    
    if places:
        # Initialize data exporter
        exporter = DataExporter(output_dir="data/output")
        
        # Export to all formats
        print("\nExporting data...")
        results = exporter.export_all_formats(places, "places")
        
        print("\nExported files:")
        for format_type, filepath in results.items():
            print(f"  - {format_type}: {filepath}")
    else:
        print("No places data fetched")


if __name__ == "__main__":
    main()
