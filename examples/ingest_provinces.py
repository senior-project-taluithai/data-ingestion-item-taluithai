"""Example script for ingesting provinces data."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import ProvinceIngestor
from data_ingestion.storage import DataExporter


def main():
    """Main function to ingest provinces data."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Initialize TAT API client
    # Set TAT_API_KEY environment variable or pass it directly
    client = TATAPIClient()
    
    # Initialize province ingestor
    ingestor = ProvinceIngestor(client)
    
    # Fetch provinces data
    print("Fetching provinces data from TAT API...")
    provinces = ingestor.fetch_provinces(
        max_pages=2  # Limit to 2 pages for example (remove for all data)
    )
    
    print(f"Fetched {len(provinces)} provinces")
    
    if provinces:
        # Initialize data exporter
        exporter = DataExporter(output_dir="data/output")
        
        # Export to all formats
        print("\nExporting data...")
        results = exporter.export_all_formats(provinces, "provinces")
        
        print("\nExported files:")
        for format_type, filepath in results.items():
            print(f"  - {format_type}: {filepath}")
    else:
        print("No provinces data fetched")


if __name__ == "__main__":
    main()
