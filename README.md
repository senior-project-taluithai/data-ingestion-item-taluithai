# Data Ingestion - Item Tower (Taluithai)

A data ingestion system for the **item tower** of a two-tower recommendation system in the Taluithai project. This system ingests tourism data from TAT (Tourism Authority of Thailand - การท่องเที่ยวแห่งประเทศไทย) including places, events, and provinces.

## Overview

This repository provides tools to:
- Fetch tourism data from TAT API (places, events, provinces)
- Transform and validate data for recommendation systems
- Export data in multiple formats (JSON, CSV, Parquet)
- Support the item tower component of a two-tower recommendation architecture

## Features

- **Comprehensive Data Models**: Pydantic models for Places, Events, and Provinces with full validation
- **TAT API Client**: Robust HTTP client with retry logic and error handling
- **Data Ingestors**: Specialized ingestors for each data type with pagination support
- **Multi-format Export**: Export to JSON, CSV, and Parquet formats
- **Flexible Configuration**: Environment-based configuration for API credentials and settings
- **Logging**: Built-in logging for monitoring ingestion processes

## Project Structure

```
data-ingestion-item-taluithai/
├── src/
│   └── data_ingestion/
│       ├── models/          # Data models (Place, Event, Province)
│       ├── ingestors/       # Data ingestion classes
│       ├── storage/         # Data export functionality
│       └── utils/           # Utilities (TAT client, logging)
├── examples/                # Example scripts
├── config/                  # Configuration files
├── data/
│   └── output/             # Output directory for exported data
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
└── setup.py               # Package setup
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/senior-project-taluithai/data-ingestion-item-taluithai.git
cd data-ingestion-item-taluithai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

3. Configure API credentials:
```bash
cp config/.env.example .env
# Edit .env and add your TAT API key
```

## Configuration

Set up your environment variables in `.env` file:

```bash
# Required: TAT API Key
TAT_API_KEY=your_api_key_here

# Optional: Override default API base URL
TAT_API_BASE_URL=https://tatapi.tourismthailand.org/tatapi/v5

# Optional: Set logging level
LOG_LEVEL=INFO

# Optional: Set output directory
OUTPUT_DIR=data/output
```

## Usage

### Quick Start

Run the all-in-one ingestion script:

```bash
python examples/ingest_all.py
```

This will ingest all data types (provinces, places, events) and export them to `data/output/`.

### Individual Data Types

Ingest specific data types:

```bash
# Ingest places only
python examples/ingest_places.py

# Ingest events only
python examples/ingest_events.py

# Ingest provinces only
python examples/ingest_provinces.py
```

### Programmatic Usage

```python
from data_ingestion.utils import setup_logging
from data_ingestion.utils.tat_client import TATAPIClient
from data_ingestion.ingestors import PlaceIngestor
from data_ingestion.storage import DataExporter

# Setup
setup_logging(level="INFO")
client = TATAPIClient(api_key="your_api_key")

# Ingest places
ingestor = PlaceIngestor(client)
places = ingestor.fetch_places(province="Bangkok", max_pages=10)

# Export data
exporter = DataExporter(output_dir="data/output")
exporter.export_to_json(places, "bangkok_places.json")
exporter.export_to_csv(places, "bangkok_places.csv")
exporter.export_to_parquet(places, "bangkok_places.parquet")
```

## Data Models

### Place Model
Represents tourist attractions and places:
- Basic information: ID, name (Thai/English), description
- Location: Province, GPS coordinates, address
- Metadata: Category, tags, images, website, contact
- Timestamps: Created/updated dates

### Event Model
Represents tourism events and festivals:
- Basic information: ID, name (Thai/English), description
- Event details: Start/end dates, location
- Metadata: Category, tags, images, website, contact
- Timestamps: Created/updated dates

### Province Model
Represents Thai provinces:
- Basic information: ID, name (Thai/English), description
- Geographic data: Region, location, area, population
- Metadata: Tags, images
- Timestamps: Created/updated dates

## Output Formats

Exported data is available in three formats:

1. **JSON**: Human-readable, nested structure
2. **CSV**: Spreadsheet-compatible, flattened structure
3. **Parquet**: Efficient columnar format for big data processing

## API Reference

### TATAPIClient

Main client for TAT API interactions:
- `get_places()`: Fetch places with filtering
- `get_events()`: Fetch events with filtering
- `get_provinces()`: Fetch provinces
- `get_place_by_id()`: Fetch specific place
- `get_event_by_id()`: Fetch specific event
- `get_province_by_id()`: Fetch specific province

### Ingestors

- `PlaceIngestor`: Handles place data ingestion
- `EventIngestor`: Handles event data ingestion
- `ProvinceIngestor`: Handles province data ingestion

### DataExporter

Export functionality:
- `export_to_json()`: Export to JSON format
- `export_to_csv()`: Export to CSV format
- `export_to_parquet()`: Export to Parquet format
- `export_all_formats()`: Export to all formats at once

## Use Cases

This data ingestion system is designed for:

1. **Two-Tower Recommendation Systems**: Provides item tower data for tourist recommendations
2. **Tourism Analytics**: Aggregate and analyze Thai tourism data
3. **Search Systems**: Build search indices for places and events
4. **Data Pipelines**: Feed data into ML/AI pipelines
5. **Tourism Applications**: Power tourism apps and websites

## Architecture Notes

This repository focuses on the **item tower** component of a two-tower recommendation system:

- **Item Tower**: Processes and represents items (places, events) with their features
- **User Tower**: (Separate repository) Processes user preferences and behavior

The two towers work together to generate personalized recommendations by matching user preferences with item characteristics.

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/data_ingestion
```

### Code Style

This project follows Python best practices:
- Type hints for better code clarity
- Pydantic for data validation
- Comprehensive logging
- Error handling and retries

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the Taluithai senior project.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- TAT (Tourism Authority of Thailand) for providing the tourism data API
- Taluithai project team