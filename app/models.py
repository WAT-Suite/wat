from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    type = Column(String, nullable=False)
    destroyed = Column(Integer, nullable=False)
    abandoned = Column(Integer, nullable=False)
    captured = Column(Integer, nullable=False)
    damaged = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("country", "type", "date", name="uq_equipment_country_type_date"),
    )


class AllEquipment(Base):
    __tablename__ = "all_equipment"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    type = Column(String, nullable=False)
    destroyed = Column(Integer, nullable=False)
    abandoned = Column(Integer, nullable=False)
    captured = Column(Integer, nullable=False)
    damaged = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("country", "type", name="uq_all_equipment_country_type"),
    )


class System(Base):
    __tablename__ = "system"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    system = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=False)
    date = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("country", "system", "url", "date", name="uq_system_country_system_url_date"),
    )


class AllSystem(Base):
    __tablename__ = "all_system"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    system = Column(String, nullable=False)
    destroyed = Column(Integer, nullable=False)
    abandoned = Column(Integer, nullable=False)
    captured = Column(Integer, nullable=False)
    damaged = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("country", "system", name="uq_all_system_country_system"),
    )
