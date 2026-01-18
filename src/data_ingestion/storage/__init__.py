"""Data storage and export functionality."""

import json
import logging
from typing import List, Union
from pathlib import Path
import pandas as pd

from ..models import Place, Event, Province

logger = logging.getLogger(__name__)


class DataExporter:
    """Export data to various formats."""
    
    def __init__(self, output_dir: str = "data/output"):
        """
        Initialize data exporter.
        
        Args:
            output_dir: Directory to save exported data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_json(
        self,
        data: List[Union[Place, Event, Province]],
        filename: str,
        indent: int = 2
    ) -> str:
        """
        Export data to JSON file.
        
        Args:
            data: List of data models
            filename: Output filename
            indent: JSON indentation level
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        try:
            # Convert pydantic models to dict
            json_data = [item.model_dump(mode='json') for item in data]
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=indent, ensure_ascii=False)
            
            logger.info(f"Exported {len(data)} items to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            raise
    
    def export_to_csv(
        self,
        data: List[Union[Place, Event, Province]],
        filename: str
    ) -> str:
        """
        Export data to CSV file.
        
        Args:
            data: List of data models
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        try:
            # Convert pydantic models to dict
            dict_data = [item.model_dump(mode='json') for item in data]
            
            # Create DataFrame
            df = pd.json_normalize(dict_data)
            
            # Export to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            logger.info(f"Exported {len(data)} items to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Failed to export to CSV: {e}")
            raise
    
    def export_to_parquet(
        self,
        data: List[Union[Place, Event, Province]],
        filename: str
    ) -> str:
        """
        Export data to Parquet file.
        
        Args:
            data: List of data models
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        try:
            # Convert pydantic models to dict
            dict_data = [item.model_dump(mode='json') for item in data]
            
            # Create DataFrame
            df = pd.json_normalize(dict_data)
            
            # Export to Parquet
            df.to_parquet(output_path, index=False, engine='pyarrow')
            
            logger.info(f"Exported {len(data)} items to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Failed to export to Parquet: {e}")
            raise
    
    def export_all_formats(
        self,
        data: List[Union[Place, Event, Province]],
        base_filename: str
    ) -> dict:
        """
        Export data to all supported formats.
        
        Args:
            data: List of data models
            base_filename: Base filename (without extension)
            
        Returns:
            Dictionary mapping format to file path
        """
        results = {}
        
        try:
            results['json'] = self.export_to_json(data, f"{base_filename}.json")
        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")
        
        try:
            results['csv'] = self.export_to_csv(data, f"{base_filename}.csv")
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
        
        try:
            results['parquet'] = self.export_to_parquet(data, f"{base_filename}.parquet")
        except Exception as e:
            logger.error(f"Failed to export Parquet: {e}")
        
        return results
