"""Data ingestors for TAT data."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models import Place, Event, Province, Location
from ..utils.tat_client import TATAPIClient

logger = logging.getLogger(__name__)


class BaseIngestor:
    """Base class for data ingestors."""
    
    def __init__(self, client: TATAPIClient):
        """
        Initialize ingestor.
        
        Args:
            client: TAT API client instance
        """
        self.client = client
    
    def _parse_location(self, data: Dict[str, Any]) -> Optional[Location]:
        """
        Parse location data.
        
        Args:
            data: Raw location data
            
        Returns:
            Location model or None
        """
        try:
            return Location(
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
                address=data.get("address")
            )
        except Exception as e:
            logger.warning(f"Failed to parse location: {e}")
            return None
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        Parse datetime string.
        
        Args:
            date_str: Date string
            
        Returns:
            Datetime object or None
        """
        if not date_str:
            return None
        
        try:
            # Try multiple datetime formats
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        except Exception as e:
            logger.warning(f"Failed to parse datetime '{date_str}': {e}")
            return None


class PlaceIngestor(BaseIngestor):
    """Ingestor for place/attraction data."""
    
    def fetch_places(
        self,
        province: Optional[str] = None,
        category: Optional[str] = None,
        max_pages: Optional[int] = None
    ) -> List[Place]:
        """
        Fetch and parse places data.
        
        Args:
            province: Filter by province name
            category: Filter by category
            max_pages: Maximum number of pages to fetch (None for all)
            
        Returns:
            List of Place models
        """
        places = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            try:
                logger.info(f"Fetching places page {page}")
                response = self.client.get_places(
                    province=province,
                    category=category,
                    page=page
                )
                
                items = response.get("result", [])
                if not items:
                    break
                
                for item in items:
                    try:
                        place = self._parse_place(item)
                        places.append(place)
                    except Exception as e:
                        logger.error(f"Failed to parse place: {e}")
                        continue
                
                page += 1
                
                # Check if there are more pages
                if len(items) < 100:  # Assuming 100 is the page size
                    break
                    
            except Exception as e:
                logger.error(f"Failed to fetch places page {page}: {e}")
                break
        
        logger.info(f"Fetched {len(places)} places")
        return places
    
    def _parse_place(self, data: Dict[str, Any]) -> Place:
        """
        Parse place data from API response.
        
        Args:
            data: Raw place data from API
            
        Returns:
            Place model
        """
        return Place(
            id=str(data.get("place_id", data.get("id", ""))),
            name=data.get("place_name", data.get("name", "")),
            name_th=data.get("place_name_th", data.get("name_th")),
            name_en=data.get("place_name_en", data.get("name_en")),
            description=data.get("place_information", data.get("description")),
            description_th=data.get("place_information_th", data.get("description_th")),
            description_en=data.get("place_information_en", data.get("description_en")),
            category=data.get("category_description", data.get("category")),
            subcategory=data.get("subcategory", []),
            province=data.get("location", {}).get("province", data.get("province")),
            province_id=data.get("province_id"),
            location=self._parse_location(data.get("location", {})),
            images=data.get("thumbnail_url", data.get("images", [])) if isinstance(data.get("thumbnail_url", data.get("images", [])), list) else [data.get("thumbnail_url")] if data.get("thumbnail_url") else [],
            website=data.get("web_url", data.get("website")),
            contact=data.get("contact", data.get("telephone")),
            tags=data.get("tags", data.get("keywords", [])),
            created_at=self._parse_datetime(data.get("created_at")),
            updated_at=self._parse_datetime(data.get("update_date", data.get("updated_at")))
        )


class EventIngestor(BaseIngestor):
    """Ingestor for event data."""
    
    def fetch_events(
        self,
        province: Optional[str] = None,
        category: Optional[str] = None,
        max_pages: Optional[int] = None
    ) -> List[Event]:
        """
        Fetch and parse events data.
        
        Args:
            province: Filter by province name
            category: Filter by category
            max_pages: Maximum number of pages to fetch (None for all)
            
        Returns:
            List of Event models
        """
        events = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            try:
                logger.info(f"Fetching events page {page}")
                response = self.client.get_events(
                    province=province,
                    category=category,
                    page=page
                )
                
                items = response.get("result", [])
                if not items:
                    break
                
                for item in items:
                    try:
                        event = self._parse_event(item)
                        events.append(event)
                    except Exception as e:
                        logger.error(f"Failed to parse event: {e}")
                        continue
                
                page += 1
                
                # Check if there are more pages
                if len(items) < 100:  # Assuming 100 is the page size
                    break
                    
            except Exception as e:
                logger.error(f"Failed to fetch events page {page}: {e}")
                break
        
        logger.info(f"Fetched {len(events)} events")
        return events
    
    def _parse_event(self, data: Dict[str, Any]) -> Event:
        """
        Parse event data from API response.
        
        Args:
            data: Raw event data from API
            
        Returns:
            Event model
        """
        return Event(
            id=str(data.get("event_id", data.get("id", ""))),
            name=data.get("event_name", data.get("name", "")),
            name_th=data.get("event_name_th", data.get("name_th")),
            name_en=data.get("event_name_en", data.get("name_en")),
            description=data.get("event_information", data.get("description")),
            description_th=data.get("event_information_th", data.get("description_th")),
            description_en=data.get("event_information_en", data.get("description_en")),
            category=data.get("category_description", data.get("category")),
            subcategory=data.get("subcategory", []),
            province=data.get("location", {}).get("province", data.get("province")),
            province_id=data.get("province_id"),
            location=self._parse_location(data.get("location", {})),
            start_date=self._parse_datetime(data.get("event_start_date", data.get("start_date"))),
            end_date=self._parse_datetime(data.get("event_end_date", data.get("end_date"))),
            images=data.get("thumbnail_url", data.get("images", [])) if isinstance(data.get("thumbnail_url", data.get("images", [])), list) else [data.get("thumbnail_url")] if data.get("thumbnail_url") else [],
            website=data.get("web_url", data.get("website")),
            contact=data.get("contact", data.get("telephone")),
            tags=data.get("tags", data.get("keywords", [])),
            created_at=self._parse_datetime(data.get("created_at")),
            updated_at=self._parse_datetime(data.get("update_date", data.get("updated_at")))
        )


class ProvinceIngestor(BaseIngestor):
    """Ingestor for province data."""
    
    def fetch_provinces(
        self,
        max_pages: Optional[int] = None
    ) -> List[Province]:
        """
        Fetch and parse provinces data.
        
        Args:
            max_pages: Maximum number of pages to fetch (None for all)
            
        Returns:
            List of Province models
        """
        provinces = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            try:
                logger.info(f"Fetching provinces page {page}")
                response = self.client.get_provinces(page=page)
                
                items = response.get("result", [])
                if not items:
                    break
                
                for item in items:
                    try:
                        province = self._parse_province(item)
                        provinces.append(province)
                    except Exception as e:
                        logger.error(f"Failed to parse province: {e}")
                        continue
                
                page += 1
                
                # Check if there are more pages
                if len(items) < 100:  # Assuming 100 is the page size
                    break
                    
            except Exception as e:
                logger.error(f"Failed to fetch provinces page {page}: {e}")
                break
        
        logger.info(f"Fetched {len(provinces)} provinces")
        return provinces
    
    def _parse_province(self, data: Dict[str, Any]) -> Province:
        """
        Parse province data from API response.
        
        Args:
            data: Raw province data from API
            
        Returns:
            Province model
        """
        return Province(
            id=str(data.get("province_id", data.get("id", ""))),
            name=data.get("province_name", data.get("name", "")),
            name_th=data.get("province_name_th", data.get("name_th")),
            name_en=data.get("province_name_en", data.get("name_en")),
            region=data.get("region", data.get("region_name")),
            description=data.get("province_information", data.get("description")),
            description_th=data.get("province_information_th", data.get("description_th")),
            description_en=data.get("province_information_en", data.get("description_en")),
            location=self._parse_location(data.get("location", {})),
            population=data.get("population"),
            area=data.get("area"),
            images=data.get("thumbnail_url", data.get("images", [])) if isinstance(data.get("thumbnail_url", data.get("images", [])), list) else [data.get("thumbnail_url")] if data.get("thumbnail_url") else [],
            tags=data.get("tags", data.get("keywords", [])),
            created_at=self._parse_datetime(data.get("created_at")),
            updated_at=self._parse_datetime(data.get("update_date", data.get("updated_at")))
        )
