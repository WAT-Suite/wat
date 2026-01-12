"""
Tests for equipment endpoints and services.
"""
import pytest
from app.models import Equipment, AllEquipment
from app.enums import Countries, EquipmentType
from app.services.equipments_service import EquipmentsService


@pytest.mark.unit
def test_get_equipments_all_countries(client, db_session, sample_equipment_data):
    """Test getting equipments for all countries."""
    # Create test data
    equipment = Equipment(**sample_equipment_data)
    db_session.add(equipment)
    db_session.commit()

    # Test endpoint
    response = client.post("/api/stats/equipments/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "ukraine"
    assert data[0]["type"] == "Tanks"


@pytest.mark.unit
def test_get_equipments_filtered_by_country(client, db_session, sample_equipment_data):
    """Test getting equipments filtered by country."""
    # Create test data for different countries
    ukraine_data = sample_equipment_data.copy()
    russia_data = sample_equipment_data.copy()
    russia_data["country"] = "russia"

    db_session.add(Equipment(**ukraine_data))
    db_session.add(Equipment(**russia_data))
    db_session.commit()

    # Test Ukraine filter
    response = client.post("/api/stats/equipments/ukraine")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "ukraine"


@pytest.mark.unit
def test_get_equipments_filtered_by_type(client, db_session, sample_equipment_data):
    """Test getting equipments filtered by type."""
    # Create test data with different types
    tanks_data = sample_equipment_data.copy()
    aircraft_data = sample_equipment_data.copy()
    aircraft_data["type"] = "Aircraft"

    db_session.add(Equipment(**tanks_data))
    db_session.add(Equipment(**aircraft_data))
    db_session.commit()

    # Test type filter
    response = client.post(
        "/api/stats/equipments/all",
        json={"types": [EquipmentType.TANKS.value]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "Tanks"


@pytest.mark.unit
def test_get_equipments_filtered_by_date(client, db_session, sample_equipment_data):
    """Test getting equipments filtered by date range."""
    # Create test data with different dates
    date1_data = sample_equipment_data.copy()
    date1_data["date"] = "2023-01-01"
    date2_data = sample_equipment_data.copy()
    date2_data["date"] = "2023-02-01"

    db_session.add(Equipment(**date1_data))
    db_session.add(Equipment(**date2_data))
    db_session.commit()

    # Test date filter
    response = client.post(
        "/api/stats/equipments/all",
        json={"date": ["2023-01-01", "2023-01-31"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == "2023-01-01"


@pytest.mark.unit
def test_get_equipments_invalid_date_range(client):
    """Test getting equipments with invalid date range."""
    response = client.post(
        "/api/stats/equipments/all",
        json={"date": ["2023-02-01", "2023-01-01"]},  # End before start
    )
    assert response.status_code == 400


@pytest.mark.unit
def test_get_total_equipments(client, db_session, sample_all_equipment_data):
    """Test getting total equipments."""
    # Create test data
    equipment = AllEquipment(**sample_all_equipment_data)
    db_session.add(equipment)
    db_session.commit()

    # Test endpoint
    response = client.post("/api/stats/equipments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total"] == 200


@pytest.mark.unit
def test_get_total_equipments_filtered(client, db_session, sample_all_equipment_data):
    """Test getting total equipments with filters."""
    # Create test data
    ukraine_data = sample_all_equipment_data.copy()
    russia_data = sample_all_equipment_data.copy()
    russia_data["country"] = "russia"

    db_session.add(AllEquipment(**ukraine_data))
    db_session.add(AllEquipment(**russia_data))
    db_session.commit()

    # Test with country filter
    response = client.post(
        "/api/stats/equipments",
        json={"country": Countries.UKRAINE.value},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "ukraine"


@pytest.mark.unit
def test_get_equipment_types(client, db_session, sample_all_equipment_data):
    """Test getting equipment types."""
    # Create test data
    equipment = AllEquipment(**sample_all_equipment_data)
    db_session.add(equipment)
    db_session.commit()

    # Test endpoint
    response = client.get("/api/stats/equipment-types")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "Tanks"


@pytest.mark.unit
def test_equipments_service_get_equipments(db_session, sample_equipment_data):
    """Test EquipmentsService.get_equipments method."""
    service = EquipmentsService(db_session)

    # Create test data
    equipment = Equipment(**sample_equipment_data)
    db_session.add(equipment)
    db_session.commit()

    # Test service method
    results = service.get_equipments(Countries.ALL)
    assert len(results) == 1
    assert results[0].country == "ukraine"


@pytest.mark.unit
def test_equipments_service_invalid_date_range(db_session, sample_equipment_data):
    """Test EquipmentsService with invalid date range."""
    service = EquipmentsService(db_session)

    equipment = Equipment(**sample_equipment_data)
    db_session.add(equipment)
    db_session.commit()

    # Test with invalid date range
    with pytest.raises(ValueError, match="Start date should be before end date"):
        service.get_equipments(
            Countries.ALL,
            date=["2023-02-01", "2023-01-01"],
        )
