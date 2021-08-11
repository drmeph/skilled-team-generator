# Balancing Algorithm
## Initialization
1) Use the file provided as input, format must be respected
2) Convert each record into a [Player](../skilled_team/player.py) then compile the [Stats](../skilled_team/stats.py)
3) Generate a weight map (mapping pid to sk_total) and uses it as input to the [bin packing](https://pypi.org/project/binpacking/)
's to_constant_bin_number method, which returns a set of teams balanced using the sk_total value. We then use that set to 
   create a list of [Team](../skilled_team/team.py)
   
![balancing](balancing-part1.png)