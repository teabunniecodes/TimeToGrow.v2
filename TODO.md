Set up database of plants to check if user has a plant or not
start working on api.py and see how much I can reconnect to JS
Set up bits redemptions

set up all the databases:
    plants_table (this will have the data counted at end of stream when user goes off line and inputted into a stats table)
        id, broadcaster_id, plant_id (can this just be the id?) timestamp_created, placement
    victim_of_table (need to look over this and may combine with other tables)
        plant_id, plant_owner_id, attacker_id, timestamp_wilted
    successfully_wilted_table (currently this is for successful attacks that result in death of plant without any watering in between)
        attacker_id, plant_id, timestamp_wilted

should we keep a tally of who kills who how many times?
what other information do we need to keep track of?