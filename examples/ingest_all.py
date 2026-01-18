"""Example script for ingesting all data types."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import PlaceIngestor, EventIngestor, ProvinceIngestor
from data_ingestion.storage import DataExporter


def main():
    """Main function to ingest all data types."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Initialize TAT API client
    client = TATAPIClient()
    
    # Initialize data exporter
    exporter = DataExporter(output_dir="data/output")
    
    # Ingest provinces
    print("=" * 60)
    print("Ingesting Provinces Data")
    print("=" * 60)
    province_ingestor = ProvinceIngestor(client)
    provinces = province_ingestor.fetch_provinces(max_pages=2)
    if provinces:
        exporter.export_all_formats(provinces, "provinces")
        print(f"✓ Exported {len(provinces)} provinces")
    
    # Ingest places
    print("\n" + "=" * 60)
    print("Ingesting Places Data")
    print("=" * 60)
    place_ingestor = PlaceIngestor(client)
    places = place_ingestor.fetch_places(max_pages=5)
    if places:
        exporter.export_all_formats(places, "places")
        print(f"✓ Exported {len(places)} places")
    
    # Ingest events
    print("\n" + "=" * 60)
    print("Ingesting Events Data")
    print("=" * 60)
    event_ingestor = EventIngestor(client)
    events = event_ingestor.fetch_events(max_pages=5)
    if events:
        exporter.export_all_formats(events, "events")
        print(f"✓ Exported {len(events)} events")
    
    # Summary
    print("\n" + "=" * 60)
    print("Ingestion Summary")
    print("=" * 60)
    print(f"Total Provinces: {len(provinces)}")
    print(f"Total Places: {len(places)}")
    print(f"Total Events: {len(events)}")
    print(f"Total Items: {len(provinces) + len(places) + len(events)}")
    print("\nAll data exported to: data/output/")


if __name__ == "__main__":
    main()
