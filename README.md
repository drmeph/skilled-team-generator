# Skilled Team Generator
Given N players, ranked according to M skills, build a T teams as even as possible

![](skilled-team-logo.png)

This project combine 2 techniques:
* [Bin Packing or Multiple Knapsacks](https://pypi.org/project/binpacking/) to create a first set of teams only balanced based on their <em>total skill value</em>:

> How can we distribute the items to exactly N bins where each carries items that sum up to approximately equal weight?

* [K-means balancing technique](https://en.wikipedia.org/wiki/K-means_clustering) which is not exactly k-means clustering but re-uses some of its concepts, like:
    
    * Random data point picking
    * Swapping data points between clusters
    * Iterate until the data become stable

## Pre-requisite
* App created using Python 3
* Check [Requirement File](requirements.txt) for the list of libraries
## Get Started
### Configuration
The [configuration file](app-config.yml) can be found in the root directory of the project

|Attribute|Type|Description|
| --- | --- | --- |
|skilled_team.log_level|str|Log level: 'INFO', 'DEBUG', 'WARNING', 'ERROR'|
|skilled_team.one_size_validation|bool|During the balancing phase, the validator check that the players' swap between teams is improving the team(s) balance. This attribute allow the user to decide if one or both sides are required. <strong>if True = One Side, if False = Both Sides. default True</strong>|
|skilled_team.player_id_index|int|Column number of the player id|
|skilled_team.first_name|int|Column number of the first name|
|skilled_team.last_name|int|Column number of the last name|
|skilled_team.skills.indexes|list(int)|List of the skills' column number|
|skilled_team.skills.manual_weights|list(int)|By default the app calculate the weight of each skill, but the user can set these manually by using this attribute, the higher the value the more important the corresponding skill will be. example: [1, 3, 2, 6, 5, 4], default: None|
|skilled_team.players_per_team|int|Maximum number of players per team|
|skilled_team.balancer.min_val_sk_set_size|int|Number of skills that the app will need to see improved after swapping players in order to consider it successful|
|skilled_team.balancer.max_failures|int|Maximum amount of consecutive failures for the app to stop the balancing process|

### Input & Output
In order to run the <em>skilled team generator</em> requires a csv file with the data containing the following fields. you can take a look at and used [the sample data](data/sample-data.csv) in the data directory
> IMPORTANT: ALL FIELDS ARE REQUIRED

|Attributes|Type|Description|
| --- | --- | --- |
|Player Id|str|Player's identifier|
|Firstname|str|Player's first name|
|Lastname|str|Player's last name|
|<skill 1 to N>|str|The user can experiment with as many skills as necessary, but keep in mind that the complexity and computation cost will increase with proportionally to the amount of skills. The app was created and tested using a set of 6 skills. Note: skills can be named as the user please.|

The <em>skilled team generator</em> will then generate 2 json output files:
* output: contains the list of teams
* stats-output: contains [the stats](#stats) compiled and used by the app to create the teams

### Run Generator
```python
python team_generator.py --output=[path_to_output_file] path_to_input_file
```
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
|team_id|int|Team identifier|
|sk_total_list|list ( int )|List containing the sum of each skill (summed by player)|
|weighted_sk_total|int|total of all skills across the team multiplied by the corresponding weight|
|player_list|Dict (key: player id, value: Player)|dictionary of all the players mapped by eid|

### <a name="stats">Stats</a>
|Attributes|Type|Description|
| --- | --- | --- |
|total_players|int|Total number of players|
|total_teams|int|Total number of teams|
|min_val_sk_set_size|int|The minimum amount of skills used for validation|
|one_side_validation|bool|True: One side validation, False: Two sides validation|
|avg_sk_list|list( float )|List of average value calculated per skill|
|sk_weight_list|list( int )|List of weight per skill calculated base on the average frequency of each skill within the dataset|
|avg_team_weight_sk_total|float|the average of weighted skill total across all teams|
|players_per_team|int|Number of players per team|
|successful_swaps|int|The amount of successful swaps applied to the team's list|