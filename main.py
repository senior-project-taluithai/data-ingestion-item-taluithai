#!/usr/bin/env python3
"""
Main CLI entry point for data ingestion.

Usage:
    python main.py --type all
    python main.py --type places --province Bangkok
    python main.py --type events --max-pages 10
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import PlaceIngestor, EventIngestor, ProvinceIngestor
from data_ingestion.storage import DataExporter


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="TAT Data Ingestion CLI for Item Tower"
    )
    
    parser.add_argument(
        "--type",
        choices=["all", "places", "events", "provinces"],
        default="all",
        help="Type of data to ingest (default: all)"
    )
    
    parser.add_argument(
        "--province",
        help="Filter by province name"
    )
    
    parser.add_argument(
        "--category",
        help="Filter by category"
    )
    
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to fetch (default: all)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="data/output",
        help="Output directory for exported data (default: data/output)"
    )
    
    parser.add_argument(
        "--format",
        choices=["all", "json", "csv", "parquet"],
        default="all",
        help="Export format (default: all)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Initialize TAT API client
    client = TATAPIClient()
    
    # Initialize data exporter
    exporter = DataExporter(output_dir=args.output_dir)
    
    # Track results
    results = {}
    
    # Ingest data based on type
    if args.type in ["all", "provinces"]:
        print("=" * 60)
        print("Ingesting Provinces Data")
        print("=" * 60)
        ingestor = ProvinceIngestor(client)
        provinces = ingestor.fetch_provinces(max_pages=args.max_pages)
        
        if provinces:
            if args.format == "all":
                results["provinces"] = exporter.export_all_formats(provinces, "provinces")
            elif args.format == "json":
                results["provinces"] = {"json": exporter.export_to_json(provinces, "provinces.json")}
            elif args.format == "csv":
                results["provinces"] = {"csv": exporter.export_to_csv(provinces, "provinces.csv")}
            elif args.format == "parquet":
                results["provinces"] = {"parquet": exporter.export_to_parquet(provinces, "provinces.parquet")}
            print(f"✓ Exported {len(provinces)} provinces\n")
    
    if args.type in ["all", "places"]:
        print("=" * 60)
        print("Ingesting Places Data")
        print("=" * 60)
        ingestor = PlaceIngestor(client)
        places = ingestor.fetch_places(
            province=args.province,
            category=args.category,
            max_pages=args.max_pages
        )
        
        if places:
            if args.format == "all":
                results["places"] = exporter.export_all_formats(places, "places")
            elif args.format == "json":
                results["places"] = {"json": exporter.export_to_json(places, "places.json")}
            elif args.format == "csv":
                results["places"] = {"csv": exporter.export_to_csv(places, "places.csv")}
            elif args.format == "parquet":
                results["places"] = {"parquet": exporter.export_to_parquet(places, "places.parquet")}
            print(f"✓ Exported {len(places)} places\n")
    
    if args.type in ["all", "events"]:
        print("=" * 60)
        print("Ingesting Events Data")
        print("=" * 60)
        ingestor = EventIngestor(client)
        events = ingestor.fetch_events(
            province=args.province,
            category=args.category,
            max_pages=args.max_pages
        )
        
        if events:
            if args.format == "all":
                results["events"] = exporter.export_all_formats(events, "events")
            elif args.format == "json":
                results["events"] = {"json": exporter.export_to_json(events, "events.json")}
            elif args.format == "csv":
                results["events"] = {"csv": exporter.export_to_csv(events, "events.csv")}
            elif args.format == "parquet":
                results["events"] = {"parquet": exporter.export_to_parquet(events, "events.parquet")}
            print(f"✓ Exported {len(events)} events\n")
    
    # Print summary
    print("=" * 60)
    print("Ingestion Complete")
    print("=" * 60)
    
    for data_type, formats in results.items():
        print(f"\n{data_type.capitalize()}:")
        for fmt, filepath in formats.items():
            print(f"  [{fmt}] {filepath}")
    
    print(f"\nAll data exported to: {args.output_dir}/")


if __name__ == "__main__":
    main()
