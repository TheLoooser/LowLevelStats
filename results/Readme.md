# How to interpret the results
For example, lets analyse the result from [*Don Noway*](https://www.twitch.tv/noway4u_sir) (aka Noway4u), a German 
High-Elo Lol Streamer.
![image goes here](Don%20Noway.png)

### Header
- Summoner name  
- Summoner information  
- Basic stats about the overall summoner level

### Body
- Top-left:  
This plot shows the percentage of games with players below a certain level. E.g. in over 80% of the games there was
at least one low level player (i.e. a player with summoner level under 100). And in over 50% of the games, there was at 
least one player whose level is smaller than 50\. Out of those roughly 52%, approximately 33% of the games had one
player whose level is under 50, ~15% of the games have two players whose level is under 50 and in 4% of the games, there
are even three players with a summoner level under 50.  


- Top-right:  
This graphic shows the distribution of levels over all players (from the selected players Solo/Duo match history). Note
that the first bar only represents 20 levels, because you are not eligible to play ranked games before level 30.  
The spike in the middle is due to the inclusion of the selected summoner. I.e. the selected players level appears in 
each match, thus making this bar considerably higher than the others.  


- Bottom-left:  
This plot shows the correlation of a players level and his rank (his current rank and not the rank a plyer had when
playing the match). The different colors represent the different ranks and each rank is split in four divisions, except
for the four last ranks (i.e. yellow, red and purple in the graph). This also explains why the ranked emblems on the
y-axis are not properly placed. However, for 99% of all players this should be fine, since those highest three ranks
account for less than 1% of the player base ([Source](https://www.leagueofgraphs.com/rankings/rank-distribution)). In
other words, for the vast majority of players, you will not encounter this faulty visualisation¹.  


- Bottom-right:  
This graph depicts the average level per role. 




¹: This is also why I did not bother fixing this problem.