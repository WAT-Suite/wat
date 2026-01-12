-- Add unique constraints for incremental updates

-- Equipment: unique by country, type, and date
ALTER TABLE equipment
ADD CONSTRAINT uq_equipment_country_type_date 
UNIQUE (country, type, date);

-- AllEquipment: unique by country and type
ALTER TABLE all_equipment
ADD CONSTRAINT uq_all_equipment_country_type 
UNIQUE (country, type);

-- System: unique by country, system, url, and date
ALTER TABLE system
ADD CONSTRAINT uq_system_country_system_url_date 
UNIQUE (country, system, url, date);

-- AllSystem: unique by country and system
ALTER TABLE all_system
ADD CONSTRAINT uq_all_system_country_system 
UNIQUE (country, system);
