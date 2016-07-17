# MinorLeagueBot
Monitors and displays stats for players and teams within a minor league farm system. Stats currently are posted to Reddit.

Specific teams and players are defined in watchlist.py. The bot can also watch for specific stats defined in watchlist.py to include
that player in the stats listing. An example is if a player hits a homerun or records 3 hits or 3 RBIs then they are included in the stats.
If that is unwanted, set the values high, minimum values may include all players from that team. Batting and pitching are looked at seperately.


In defining the team, you specify the 'division code'. It's typically a 3 character identifier and can be found in the path of a gameday or box score.
'rok' and 'aaa' are examples of this code. It is needed to obtain the schedule for the team that contains information about the scheduled games. There
is a boolean value that lets the bot not run the scheduler around their reported game times. There are a few leagues that report a game time
as early in the morning, but do not play or report the results until many hours later. This is to prevent the bot from running needlessly until those
stats are reported. If all teams are finished or all remaining games are not being watched by the scheduler it updates on a 1 hour interval until
all games have completed. 

When running, the bot checks the current date and uses an hour offset to adjust for varying time zones. It queries for the scheduled games for that 
date and any further dates specified. In the current iteration only the current date is asked. When it grabs the scheduled information it
contains necessary information about the game identifier needed to grab both the line score and box score information. Once ran it checks
each roster for names in the watch list, this is mainly for batters as pitchers aren't expected every game, if the name is on the roster
but they aren't listed in the box score, then they are added to a did not play list. Injured lists are also checked to see which players are
currently injured.

The watch list can have players not in the farm system without any negative results. If you were to supply the current major league roster, it
would monitor and pickup any player that is on a rehab assignment in the minors.

Once the information is gathered a post is generated and results are posted to reddit currently. The update interval is used when a game is currently
being played. If no games are being played the bot either sleeps until 15 minutes before the next start if the team is being watched by the scheduler
or ends if all games are finished. 

![alt tag](http://i.imgur.com/EIW5wUL.png)

Example of the bot running. Current games try to grab game day and radio stream listed in the game information obtained from the schedule. The frequency
of updates provided by the box or line score is dependent on the team. Some lower levels don't update on a pitch by pitch basis so it may only
update that box score every half inning or after the end of a game. 

A team link and player link is provided for each team or player being watched. When adding players to the watch list the name should appear exactly how it appears on their MILB page.
