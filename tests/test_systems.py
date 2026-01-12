"""
Tests for system endpoints and services.
"""
import pytest
from app.models import System, AllSystem
from app.enums import Countries, Status
from app.services.systems_service import SystemsService


@pytest.mark.unit
def test_get_systems_by_country(client, db_session, sample_system_data):
    """Test getting systems by country."""
    # Create test data
    system = System(**sample_system_data)
    db_session.add(system)
    db_session.commit()

    # Test endpoint
    response = client.post("/api/stats/systems/ukraine")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "ukraine"
    assert data[0]["system"] == "M1 Abrams"


@pytest.mark.unit
def test_get_systems_filtered_by_system(client, db_session, sample_system_data):
    """Test getting systems filtered by system name."""
    # Create test data with different systems
    system1_data = sample_system_data.copy()
    system2_data = sample_system_data.copy()
    system2_data["system"] = "Leopard 2"

    db_session.add(System(**system1_data))
    db_session.add(System(**system2_data))
    db_session.commit()

    # Test system filter
    response = client.post(
        "/api/stats/systems/ukraine",
        json={"systems": ["M1 Abrams"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["system"] == "M1 Abrams"


@pytest.mark.unit
def test_get_systems_filtered_by_status(client, db_session, sample_system_data):
    """Test getting systems filtered by status."""
    # Create test data with different statuses
    destroyed_data = sample_system_data.copy()
    captured_data = sample_system_data.copy()
    captured_data["status"] = "captured"

    db_session.add(System(**destroyed_data))
    db_session.add(System(**captured_data))
    db_session.commit()

    # Test status filter
    response = client.post(
        "/api/stats/systems/ukraine",
        json={"status": [Status.DESTROYED.value]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "destroyed"


@pytest.mark.unit
def test_get_systems_filtered_by_date(client, db_session, sample_system_data):
    """Test getting systems filtered by date range."""
    # Create test data with different dates
    date1_data = sample_system_data.copy()
    date1_data["date"] = "2023-01-01"
    date2_data = sample_system_data.copy()
    date2_data["date"] = "2023-02-01"

    db_session.add(System(**date1_data))
    db_session.add(System(**date2_data))
    db_session.commit()

    # Test date filter
    response = client.post(
        "/api/stats/systems/ukraine",
        json={"date": ["2023-01-01", "2023-01-31"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == "2023-01-01"


@pytest.mark.unit
def test_get_systems_invalid_date_range(client):
    """Test getting systems with invalid date range."""
    response = client.post(
        "/api/stats/systems/ukraine",
        json={"date": ["2023-02-01", "2023-01-01"]},  # End before start
    )
    assert response.status_code == 400


@pytest.mark.unit
def test_get_total_systems(client, db_session, sample_all_system_data):
    """Test getting total systems."""
    # Create test data
    system = AllSystem(**sample_all_system_data)
    db_session.add(system)
    db_session.commit()

    # Test endpoint
    response = client.post("/api/stats/systems")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total"] == 9


@pytest.mark.unit
def test_get_total_systems_filtered(client, db_session, sample_all_system_data):
    """Test getting total systems with filters."""
    # Create test data
    ukraine_data = sample_all_system_data.copy()
    russia_data = sample_all_system_data.copy()
    russia_data["country"] = "russia"

    db_session.add(AllSystem(**ukraine_data))
    db_session.add(AllSystem(**russia_data))
    db_session.commit()

    # Test with country filter
    response = client.post(
        "/api/stats/systems",
        json={"country": Countries.UKRAINE.value},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "ukraine"


@pytest.mark.unit
def test_get_system_types(client, db_session, sample_all_system_data):
    """Test getting system types."""
    # Create test data
    system = AllSystem(**sample_all_system_data)
    db_session.add(system)
    db_session.commit()

    # Test endpoint
    response = client.get("/api/stats/system-types")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["system"] == "M1 Abrams"


@pytest.mark.unit
def test_systems_service_get_systems(db_session, sample_system_data):
    """Test SystemsService.get_systems method."""
    service = SystemsService(db_session)

    # Create test data
    system = System(**sample_system_data)
    db_session.add(system)
    db_session.commit()

    # Test service method
    results = service.get_systems(Countries.UKRAINE)
    assert len(results) == 1
    assert results[0].country == "ukraine"


@pytest.mark.unit
def test_systems_service_invalid_date_range(db_session, sample_system_data):
    """Test SystemsService with invalid date range."""
    service = SystemsService(db_session)

    system = System(**sample_system_data)
    db_session.add(system)
    db_session.commit()

    # Test with invalid date range
    with pytest.raises(ValueError, match="Start date should be before end date"):
        service.get_systems(
            Countries.UKRAINE,
            date=["2023-02-01", "2023-01-01"],
        )
