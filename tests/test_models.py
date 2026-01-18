"""Basic tests for data models."""

import pytest
from datetime import datetime
from data_ingestion.models import Place, Event, Province, Location


def test_location_model():
    """Test Location model creation."""
    location = Location(
        latitude=13.7563,
        longitude=100.5018,
        address="Bangkok, Thailand"
    )
    assert location.latitude == 13.7563
    assert location.longitude == 100.5018
    assert location.address == "Bangkok, Thailand"


def test_place_model():
    """Test Place model creation."""
    place = Place(
        id="place_001",
        name="Grand Palace",
        name_th="พระบรมมหาราชวัง",
        name_en="Grand Palace",
        description="Historic royal palace",
        province="Bangkok",
        tags=["historic", "palace"]
    )
    assert place.id == "place_001"
    assert place.name == "Grand Palace"
    assert place.province == "Bangkok"
    assert len(place.tags) == 2


def test_event_model():
    """Test Event model creation."""
    event = Event(
        id="event_001",
        name="Songkran Festival",
        name_th="เทศกาลสงกรานต์",
        name_en="Songkran Festival",
        description="Thai New Year",
        province="Bangkok",
        start_date=datetime(2024, 4, 13),
        end_date=datetime(2024, 4, 15)
    )
    assert event.id == "event_001"
    assert event.name == "Songkran Festival"
    assert event.province == "Bangkok"
    assert event.start_date.day == 13


def test_province_model():
    """Test Province model creation."""
    province = Province(
        id="province_001",
        name="Bangkok",
        name_th="กรุงเทพมหานคร",
        name_en="Bangkok",
        region="Central"
    )
    assert province.id == "province_001"
    assert province.name == "Bangkok"
    assert province.region == "Central"


def test_place_with_location():
    """Test Place model with location."""
    location = Location(latitude=13.7563, longitude=100.5018)
    place = Place(
        id="place_002",
        name="Test Place",
        location=location
    )
    assert place.location is not None
    assert place.location.latitude == 13.7563
