-- Creates a table to track the currently active plants
CREATE TABLE IF NOT EXISTS plants (
    id SERIAL PRIMARY KEY,
    brodcaster_id INT,
    plant_owner_id INT,
    time_planted TIMESTAMP WITH TIME ZONE NOT NULL,
    plant_status INT, -- 0 = Dead 1 = Alive (Or would True/False be better)
    UNIQUE (broadcaster_id, plant_owner, plant_status)
);

-- Creates a table to keep track of the current placements for the alive plants in specific broadcasters stream
CREATE TABLE IF NOT EXISTS placement (
    plant_owner_id REFERENCES plant(plant_owner_id) PRIMARY KEY UNIQUE,
    placement INT,
    CHECK (REFERENCES plant(plant_status) = 1),
)

-- Creates an attacks table that keeps track of who attacks who
CREATE TABLE IF NOT EXISTS attacks (
    id SERIAL PRIMARY KEY,
    plant_id SERIAL REFERENCES plants(id),
    attacker_id INT
)

-- Creates a table track the users who successfully wilted another person's plant (aka death by attack with no watering inbetween) 
CREATE TABLE IF NOT EXISTS wilted_plants (
    id SERIAL PRIMARY KEY,
    attacked BOOLEAN,
    attacker_id REFERENCES attacks(attacker_id),
    time_wilted TIMESTAMP WITH TIME ZONE NOT NULL
)

-- Creates a table that keeps track of the players stats
CREATE TABLE IF NOT EXISTS plant_owner_stats (
    id SERIAL PRIMARY KEY,
    plant_owner_id REFERENCES plant(plant_owner_id),
    broadcaster_id REFERENCES plant(broadcaster_id),
    total_plants BIGINT,
    total_plant_time INTERVAL,
    water BIGINT,
    attacked BIGINT,
    attacker BIGINT,
    death_by_thirst BIGINT,
    death_by_attack BIGINT,
    first_place BIGINT,
    second_place BIGINT,
    third_place BIGINT,
    UNIQUE (plant_owner_id, broadcaster_id)
)