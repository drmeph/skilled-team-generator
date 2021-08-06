# Skilled Team Generator
Given N players, ranked according to M skills, build a T teams as even as possible

## Pre-requisite

## Get Started
### Configuration
### Run Generator

## Data Structures
### Player
|Attributes|Type|Description|
| --- | --- | --- |
|pid|string|Player's id|
|first_name|string|player’s first name|
|last_name|string|player’s last name|
|sk_list|list ( int (0-5) )|List of the skills’ value|
|sk_total|int|Sum of all the values from sk_list|

### Team
|Attributes|Type|Description|
| --- | --- | --- |
|sk_total_list|list ( int )|List containing the sum of each skill (summed by player)|
|weighted_sk_total|int|total of all skills across the team multiplied by the corresponding weight|
|player_list|Dict (key: player id, value: Player)|dictionary of all the players mapped by eid|

### GameStats
|Attributes|Type|Description|
| --- | --- | --- |
|total_players|int||
|total_teams|int||
|min_val_sk_set_size|int|The minimum amount of skills used for validation|
|avg_sk_list|list( float )||
|sk_weight_list|list( int )||
|avg_team_weight_sk_total|float|the average|
|players_per_team|int|Number of players per team|