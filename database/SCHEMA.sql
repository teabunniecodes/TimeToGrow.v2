-- Creates a table for tokens
CREATE TABLE IF NOT EXISTS tokens (
    user_id VARCHAR(25) PRIMARY KEY,
    token VARCHAR(250) NOT NULL,
    refresh VARCHAR(250) NOT NULL
);

-- Creates a table to track the currently active plants
CREATE TABLE IF NOT EXISTS plants (
    id SERIAL PRIMARY KEY,
    broadcaster_id INT,
    plant_owner_id INT,
    time_planted TIMESTAMP WITH TIME ZONE NOT NULL,
    plant_status INT, -- 0 = Dead 1 = Alive (Or would True/False be better)
    UNIQUE (broadcaster_id, plant_owner_id, plant_status) -- Double check this - it's wrong? may need to do Check for plant status instead
);

-- -- Creates a table to keep track of the current placements for the alive plants in specific broadcasters stream
-- CREATE TABLE IF NOT EXISTS placement (
--     plant_owner_id INT PRIMARY KEY,
--     placement INT,
--     iteration INT,
--     CHECK (REFERENCES plant(plant_status) = 1)
-- );

-- Creates an attacks table that keeps track of who attacks who
CREATE TABLE IF NOT EXISTS attacks (
    id SERIAL PRIMARY KEY,
    plant_id SERIAL REFERENCES plants(id),
    attacker_id INT
);

-- Creates a table track the users who successfully wilted another person's plant (aka death by attack with no watering inbetween) 
CREATE TABLE IF NOT EXISTS wilted_plants (
    id SERIAL PRIMARY KEY,
    attacked BOOLEAN,
    attacker_id INT,
    time_wilted TIMESTAMP WITH TIME ZONE NOT NULL
);

-- -- Creates a table that keeps track of the players stats
-- CREATE TABLE IF NOT EXISTS user_stats (
--     id SERIAL PRIMARY KEY,
--     plant_owner_id INT REFERENCES plants(plant_owner_id),
--     broadcaster_id INT REFERENCES plants(broadcaster_id),
--     total_plants BIGINT,
--     total_plant_time INTERVAL,
--     water BIGINT,
--     attacked BIGINT,
--     attacker BIGINT,
--     death_by_thirst BIGINT,
--     death_by_attack BIGINT,
--     first_place BIGINT,
--     second_place BIGINT,
--     third_place BIGINT,
--     UNIQUE (plant_owner_id, broadcaster_id)
-- );