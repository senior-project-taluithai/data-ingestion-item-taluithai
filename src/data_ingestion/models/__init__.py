"""Data models for TAT data ingestion."""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class Location(BaseModel):
    """Geographic location model."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class Place(BaseModel):
    """Place/attraction data model for item tower."""
    
    id: str = Field(..., description="Unique identifier for the place")
    name: str = Field(..., description="Place name")
    name_th: Optional[str] = Field(None, description="Place name in Thai")
    name_en: Optional[str] = Field(None, description="Place name in English")
    description: Optional[str] = Field(None, description="Place description")
    description_th: Optional[str] = Field(None, description="Description in Thai")
    description_en: Optional[str] = Field(None, description="Description in English")
    
    category: Optional[str] = Field(None, description="Place category")
    subcategory: Optional[List[str]] = Field(default_factory=list, description="Place subcategories")
    
    province: Optional[str] = Field(None, description="Province name")
    province_id: Optional[str] = Field(None, description="Province ID")
    
    location: Optional[Location] = Field(None, description="Geographic location")
    
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    website: Optional[str] = Field(None, description="Official website")
    contact: Optional[str] = Field(None, description="Contact information")
    
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for search/recommendation")
    
    created_at: Optional[datetime] = Field(None, description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "place_001",
                "name": "Grand Palace",
                "name_th": "พระบรมมหาราชวัง",
                "name_en": "Grand Palace",
                "description": "Historic royal palace complex",
                "category": "attraction",
                "province": "Bangkok",
                "location": {
                    "latitude": 13.7500,
                    "longitude": 100.4917
                },
                "tags": ["historic", "palace", "culture"]
            }
        }
    )


class Event(BaseModel):
    """Event data model for item tower."""
    
    id: str = Field(..., description="Unique identifier for the event")
    name: str = Field(..., description="Event name")
    name_th: Optional[str] = Field(None, description="Event name in Thai")
    name_en: Optional[str] = Field(None, description="Event name in English")
    description: Optional[str] = Field(None, description="Event description")
    description_th: Optional[str] = Field(None, description="Description in Thai")
    description_en: Optional[str] = Field(None, description="Description in English")
    
    category: Optional[str] = Field(None, description="Event category")
    subcategory: Optional[List[str]] = Field(default_factory=list, description="Event subcategories")
    
    province: Optional[str] = Field(None, description="Province name")
    province_id: Optional[str] = Field(None, description="Province ID")
    
    location: Optional[Location] = Field(None, description="Event location")
    
    start_date: Optional[datetime] = Field(None, description="Event start date")
    end_date: Optional[datetime] = Field(None, description="Event end date")
    
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    website: Optional[str] = Field(None, description="Official website")
    contact: Optional[str] = Field(None, description="Contact information")
    
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for search/recommendation")
    
    created_at: Optional[datetime] = Field(None, description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "event_001",
                "name": "Songkran Festival",
                "name_th": "เทศกาลสงกรานต์",
                "name_en": "Songkran Festival",
                "description": "Thai New Year water festival",
                "category": "festival",
                "province": "Bangkok",
                "start_date": "2024-04-13T00:00:00",
                "end_date": "2024-04-15T23:59:59",
                "tags": ["festival", "culture", "new year"]
            }
        }
    )


class Province(BaseModel):
    """Province data model."""
    
    id: str = Field(..., description="Unique identifier for the province")
    name: str = Field(..., description="Province name")
    name_th: Optional[str] = Field(None, description="Province name in Thai")
    name_en: Optional[str] = Field(None, description="Province name in English")
    
    region: Optional[str] = Field(None, description="Region (North, South, East, West, Central, Northeast)")
    
    description: Optional[str] = Field(None, description="Province description")
    description_th: Optional[str] = Field(None, description="Description in Thai")
    description_en: Optional[str] = Field(None, description="Description in English")
    
    location: Optional[Location] = Field(None, description="Province center location")
    
    population: Optional[int] = Field(None, description="Population")
    area: Optional[float] = Field(None, description="Area in square kilometers")
    
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for search")
    
    created_at: Optional[datetime] = Field(None, description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "province_001",
                "name": "Bangkok",
                "name_th": "กรุงเทพมหานคร",
                "name_en": "Bangkok",
                "region": "Central",
                "location": {
                    "latitude": 13.7563,
                    "longitude": 100.5018
                },
                "tags": ["capital", "urban", "central"]
            }
        }
    )
