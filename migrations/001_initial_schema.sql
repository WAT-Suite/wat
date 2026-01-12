-- Create equipment table
CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    destroyed INTEGER NOT NULL,
    abandoned INTEGER NOT NULL,
    captured INTEGER NOT NULL,
    damaged INTEGER NOT NULL,
    total INTEGER NOT NULL,
    date VARCHAR NOT NULL
);

-- Create all_equipment table
CREATE TABLE IF NOT EXISTS all_equipment (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    destroyed INTEGER NOT NULL,
    abandoned INTEGER NOT NULL,
    captured INTEGER NOT NULL,
    damaged INTEGER NOT NULL,
    total INTEGER NOT NULL
);

-- Create system table
CREATE TABLE IF NOT EXISTS system (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    origin VARCHAR NOT NULL,
    system VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    date VARCHAR NOT NULL
);

-- Create all_system table
CREATE TABLE IF NOT EXISTS all_system (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    system VARCHAR NOT NULL,
    destroyed INTEGER NOT NULL,
    abandoned INTEGER NOT NULL,
    captured INTEGER NOT NULL,
    damaged INTEGER NOT NULL,
    total INTEGER NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_equipment_country ON equipment(LOWER(country));
CREATE INDEX IF NOT EXISTS idx_equipment_type ON equipment(type);
CREATE INDEX IF NOT EXISTS idx_equipment_date ON equipment(date);

CREATE INDEX IF NOT EXISTS idx_all_equipment_country ON all_equipment(LOWER(country));
CREATE INDEX IF NOT EXISTS idx_all_equipment_type ON all_equipment(type);

CREATE INDEX IF NOT EXISTS idx_system_country ON system(LOWER(country));
CREATE INDEX IF NOT EXISTS idx_system_system ON system(system);
CREATE INDEX IF NOT EXISTS idx_system_status ON system(status);
CREATE INDEX IF NOT EXISTS idx_system_date ON system(date);

CREATE INDEX IF NOT EXISTS idx_all_system_country ON all_system(LOWER(country));
CREATE INDEX IF NOT EXISTS idx_all_system_system ON all_system(system);

-- Create migration tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
