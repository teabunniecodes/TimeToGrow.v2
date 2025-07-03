-- Creates a table for tokens
CREATE TABLE IF NOT EXISTS tokens (
    user_id TEXT PRIMARY KEY,
    token TEXT NOT NULL,
    refresh TEXT NOT NULL
);

-- Creates a table to keep track of all users
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    bits INT
);

-- Creates a table to track the currently active plants
CREATE TABLE IF NOT EXISTS plants (
    id SERIAL PRIMARY KEY,
    plant_owner_id TEXT NOT NULL REFERENCES users(user_id),
    broadcaster_id TEXT,
    time_planted TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    time_wilted TIMESTAMP DEFAULT NULL,
    number_watered INT DEFAULT 0,
    number_thugged INT DEFAULT 0,
    number_attacked INT DEFAULT 0,
    death_by TEXT DEFAULT NULL, -- Can put Thirst, attacker_id, 
    placement INT DEFAULT NULL
    -- CHECK(time_wilted == NULL)
    -- UNIQUE (broadcaster_id, plant_owner_id)-- Double check this - it's wrong? may need to do Check for plant status instead
);

-- Creates an attacks table that keeps track of who attacks who
CREATE TABLE IF NOT EXISTS attacks (
    id SERIAL PRIMARY KEY,
    attacker_id TEXT NOT NULL,
    plant_owner_id TEXT DEFAULT NULL,
    success BOOLEAN -- This will be used to find out accuracy stats
);