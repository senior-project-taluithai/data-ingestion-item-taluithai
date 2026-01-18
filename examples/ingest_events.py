"""Example script for ingesting events data."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import EventIngestor
from data_ingestion.storage import DataExporter


def main():
    """Main function to ingest events data."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Initialize TAT API client
    # Set TAT_API_KEY environment variable or pass it directly
    client = TATAPIClient()
    
    # Initialize event ingestor
    ingestor = EventIngestor(client)
    
    # Fetch events data
    print("Fetching events data from TAT API...")
    events = ingestor.fetch_events(
        province=None,  # Fetch all provinces
        category=None,  # Fetch all categories
        max_pages=5     # Limit to 5 pages for example (remove for all data)
    )
    
    print(f"Fetched {len(events)} events")
    
    if events:
        # Initialize data exporter
        exporter = DataExporter(output_dir="data/output")
        
        # Export to all formats
        print("\nExporting data...")
        results = exporter.export_all_formats(events, "events")
        
        print("\nExported files:")
        for format_type, filepath in results.items():
            print(f"  - {format_type}: {filepath}")
    else:
        print("No events data fetched")


if __name__ == "__main__":
    main()
