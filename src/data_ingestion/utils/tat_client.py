"""TAT API client for fetching tourism data."""

import os
import logging
from typing import List, Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class TATAPIClient:
    """Client for interacting with TAT (Tourism Authority of Thailand) API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize TAT API client.
        
        Args:
            api_key: API key for TAT API (can be set via TAT_API_KEY env var)
            base_url: Base URL for TAT API (can be set via TAT_API_BASE_URL env var)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key or os.getenv("TAT_API_KEY", "")
        self.base_url = base_url or os.getenv(
            "TAT_API_BASE_URL", 
            "https://tatapi.tourismthailand.org/tatapi/v5"
        )
        self.timeout = timeout
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to TAT API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_places(
        self, 
        province: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Fetch places/attractions data.
        
        Args:
            province: Filter by province name
            category: Filter by category
            page: Page number
            limit: Number of results per page
            
        Returns:
            Places data
        """
        params = {
            "numberOfResult": limit,
            "page": page
        }
        
        if province:
            params["provinceName"] = province
        if category:
            params["category"] = category
        
        return self._make_request("places", params)
    
    def get_events(
        self,
        province: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Fetch events data.
        
        Args:
            province: Filter by province name
            category: Filter by category
            page: Page number
            limit: Number of results per page
            
        Returns:
            Events data
        """
        params = {
            "numberOfResult": limit,
            "page": page
        }
        
        if province:
            params["provinceName"] = province
        if category:
            params["category"] = category
        
        return self._make_request("events", params)
    
    def get_provinces(
        self,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Fetch provinces data.
        
        Args:
            page: Page number
            limit: Number of results per page
            
        Returns:
            Provinces data
        """
        params = {
            "numberOfResult": limit,
            "page": page
        }
        
        return self._make_request("provinces", params)
    
    def get_place_by_id(self, place_id: str) -> Dict[str, Any]:
        """
        Fetch specific place by ID.
        
        Args:
            place_id: Place identifier
            
        Returns:
            Place data
        """
        return self._make_request(f"places/{place_id}")
    
    def get_event_by_id(self, event_id: str) -> Dict[str, Any]:
        """
        Fetch specific event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            Event data
        """
        return self._make_request(f"events/{event_id}")
    
    def get_province_by_id(self, province_id: str) -> Dict[str, Any]:
        """
        Fetch specific province by ID.
        
        Args:
            province_id: Province identifier
            
        Returns:
            Province data
        """
        return self._make_request(f"provinces/{province_id}")
