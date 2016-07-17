from team import Team

#current information is for the Cubs farm system. team id's and players can be adjusted for other systems
#noteable stats are what causes stats to displayed. Name in the list will force it to find the player
notable_batters = ["Javier Baez", "Eloy Jimenez", "Matt Szczur", "Christian Villanueva",
                   "Arismendy Alcantara", "Tommy La Stella", "Albert Almora", "Willson Contreras", "Billy McKinney",
                   "Jeimer Candelario", "Mark Zagunis", "Chesny Young", "Gleyber Torres", "Ian Happ", "Donnie Dewees",
                   "Dan Vogelbach", "Wladimir Galindo", "Frandy Delarosa", "Darryl Wilson", "Chris Pieters",
                   "Shawon Dunston Jr.", "Emilio Bonifacio", "Quintin Berry", "Eddy Martinez","Miguel Montero", "Munenori Kawasaki", 
				   "Yonathan Perlaza", "Jonathan Sierra", "Aramis Ademan", "Miguel Amaya", "Kwang-Min Kwon", "D.J. Wilson", "Fidel Mejia", "Jorge Soler", "Andruw Monasterio", "Ian Rice", "Dexter Fowler"]

notable_pitchers = ["Carl Edwards Jr.", "Ryan Williams", "Paul Blackburn", "Jen-Ho Tseng",
                    "Carson Sands", "Brian Schlitter", "Jonathan Martinez", "Jake Stinnett", "Pierce Johnson",
                    "Paul Blackburn", "Ryan Williams", "Tsuyoshi Wada", "Duane Underwood Jr.", "Duane Underwood","Dylan Cease",
                    "Bryan Hudson", "Justin Steele", "Corey Black", "Trevor Cahill", "Tommy Thorpe", "Neil Ramirez",
                    "Carlos Pimentel", "Oscar De La Cruz", "Gerardo Concepcion", "Brailyn Marquez", "Brian Matusz", "Faustino Carrera", "Adam Warren", "Jose Albertos", "Rob Zastryzny", "Clayton Richard"]

#noteable stats will cause any player with matching stats to be displayed if they achieve any of the following
notable_batter_hr = 1
notable_batter_hits = 3
notable_batter_rbi = 3

notable_pitcher_innings = 8.0
notable_pitcher_strikeouts = 8

#Team ids. Divisions are hardcoded to these variables. To watch a different team, change ID value - keep in division.
team_aaa_id = "451"
team_aa_id = "553"
team_azl_id = "407"
team_shortseason_id = "461"
team_lowa_id = "550"
team_higha_id = "521"
team_dsl_id = "609"
team_dsl2_id = "2270"
team_vsl_id = "652"

#Team Objects
team1 = Team("451", "aaa", False) #aaa
team2 = Team("553", "aax", False) #aa
team3 = Team("521", "afa", False) #high a
team4 = Team("550", "afx", False) #low a
team5 = Team("461", "asx", False) #shortseaon
team6 = Team("407", "rok", False) #azl
team7 = Team("609", "rok", True) #dsl 1
team8 = Team("2270", "rok", True) #dsl2
team9 = Team("652", "rok", True) #vsl not used