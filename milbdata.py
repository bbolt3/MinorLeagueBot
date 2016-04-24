import requests
import datetime
from game import Game
from inactive import InactivePlayer
from player import *
from watchlist import *
import redditpost

class MilbData():

    def date_format(self, date):
        return date.strftime('%Y/%m/%d')


    def string_to_long_date(self, string):
        date = datetime.datetime.strptime(string, "%m/%d/%Y %H:%M:%S %p")
        return "year_%s/month_%s/day_%s/" % (date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))

    def string_to_long_date(self, year, month, day):
        return "year_%s/month_%s/day_%s/" % (year, month, day)


    def get_schedule(self, start_date, end_date, team_id, season):
        """
        :param start_date: first date to look for in the schedule to search for a game
        :param end_date: last day in schedule to search for a game
        :param team_id:  specific team_id that distinguishes team from others
        :param season: year the game takes place
        :return: schedule JSON containing games happening between start and end dates
        """
        return requests.get(r"http://www.milb.com/lookup/json/named.schedule_team_complete.bam?start_date='" + start_date +
                     "'&end_date='" + end_date + "'&team_id=" + team_id + "&season=" + season).json()


    def set_game_information_from_schedule(self, current_game):
        """
        :param current_game single json of a single game pulled from the schedule:
        :return game object for a single game:
        """
        if "home_away_sw" in current_game:
                if current_game["home_away_sw"] == "H":
                    home_team = current_game["team_brief"]
                    away_team = current_game["opponent_brief"]
                else:
                    home_team = current_game["opponent_brief"]
                    away_team = current_game["team_brief"]

                game = Game(current_game["team_id"], current_game["team_full"], current_game["game_id"], home_team,
                            away_team, current_game["game_time_local"], current_game["time_zone_local"],
                            current_game['venue_name'])

                game.team_record = current_game["team_wl"]
                game.opponent_record = current_game["opponent_wl"]
                game.opponent_name_full = current_game["opponent_full"]
                #print current_game["team_full"] + "  " + current_game["game_time_local"] + "   " +  current_game["game_time_et"]
                #game_time = datetime.datetime.strptime(current_game["game_time_et"], "%Y-%m-%dT%H:%M:%S")
                game_time = datetime.datetime.strptime(current_game["team_game_time"], "%m/%d/%Y %I:%M:%S %p")
                game.scheduled_start = game_time.strftime("%I:%M %p")
                #game.scheduled_start = game_time.strftime("%I:%M:%S %p")
                #game.team_local_timezone = "EDT"

                game.team_local_timezone = current_game["team_time_zone"]
                game.double_header = current_game["double_header_sw"]
                game.game_number = current_game["game_nbr"]
                if "team_tunein" in current_game:
                    game.listen = current_game["team_tunein"]
                if "game_status" in current_game:
                    if current_game["game_status"].startswith("Postponed") or \
                            current_game["game_status"].startswith("Delayed") or \
                            current_game["game_status"].startswith("Suspended") or \
                            current_game["game_status"].startswith("Cancelled"):

                        game.game_status = "%s: %s" % (current_game["game_status"], current_game["reason"])
                    else:
                        game.game_status = current_game["game_status"]
                if "result" in current_game:
                    game.result = current_game["result"]
        return game

    def get_games(self, schedule):
        """
        :param schedule: JSON object containing teams schedule for specified dates
        :return: list of game objects for specified scheduled dates
        """
        games = []
        total_size = schedule["schedule_team_complete"]["queryResults"]["totalSize"]
        if int(total_size) != 0:
            upcoming_games = schedule["schedule_team_complete"]["queryResults"]["row"]
        if int(total_size) > 1:
            for row in upcoming_games:
                game = self.set_game_information_from_schedule(row)
                games.append(game)
        elif int(total_size) == 1:
                game = self.set_game_information_from_schedule(upcoming_games)
                games.append(game)

        return games


    def get_score_url(self, is_boxscore, game):
        """
        :param is_boxscore: True value indicates boxscore JSON URL is requested otherwise return linescore JSON URL
        :param game: game object. Game id is needed from object to get the URL
        :return: URL to either linescore or boxscore JSON
        """
        base_url = "http://www.milb.com/gdcross/components/game"
        game_id = unicode.replace(game.game_id, "/", "_")
        game_id = unicode.replace(game_id, "-", "_")
        year, month, day, oppenent, team, game_number = game_id.split("_")
        division = ""
        if game.team_id == team_aaa_id:
            division = "aaa"
        elif game.team_id == team_azl_id or game.team_id == team_dsl_id or game.team_id == team_vsl_id:
            division = "rok"
        elif game.team_id == team_shortseason_id:
            division = "asx"
        elif game.team_id == team_lowa_id:
            division = "afx"
        elif game.team_id == team_higha_id:
            division = "afa"
        elif game.team_id == team_aa_id:
            division = "aax"
        if division != "" and is_boxscore:
            return "%s/%s/%sgid_%s/boxscore.json" % (base_url, division, self.string_to_long_date(year, month, day), game_id)
            #return "%s/%s/%sgid_%s/boxscore.json" % (base_url, division, string_to_long_date(game.home_time), game_id)
        if division != "" and not is_boxscore:
            return "%s/%s/%sgid_%s/linescore.json" % (base_url, division, self.string_to_long_date(year, month, day), game_id)
            #return "%s/%s/%sgid_%s/linescore.json" % (base_url, division, string_to_long_date(game.home_time), game_id)


    def get_score_json(self, url):
        """
        :param url: URL to JSON
        :return: JSON for URL
        """
        if not url:
            return
        try:
            json = requests.get(url).json()
            return json
        except Exception, e:
            #print e.message
            return


    def get_boxscore(self, game):
            return self.get_score_json(self.get_score_url(True, game))


    def get_linescore(self, game):
            return self.get_score_json(self.get_score_url(False, game))


    def get_roster(self, team_id):
        return self.get_score_json("http://www.milb.com/lookup/json/named.roster_all.bam?team_id=" + team_id)


    def get_injury_list(self, player_list, roster):
        """
        :param player_list copy of the list of noteable players (to be watched):
        :param roster json of the roster for the team from get_roster method:
        :return list of players that were marked as inactive:
        """
        injury_list = []
        players = roster["roster_all"]["queryResults"]["row"]
        for player in players:
            if "Active" in player["status_short"] and player["name_first_last"] in player_list:
                player_list.remove(player["name_first_last"])
            if "Active" not in player["status_short"] and player["status_code"] != "RA":
                player_name = player["name_first_last"]
                if player_name in player_list:
                    injury = InactivePlayer(player["player_id"], player["name_first_last"], player["team_id"])
                    injury.injury = player["status_short"]
                    injury.position = player["position"]
                    injury_list.append(injury)
                    player_list.remove(player["name_first_last"])
        return injury_list


    def get_did_not_play(self, game, player_list, injured_batters, roster):
        """
        :param game object:
        :param player_list copy of the noteable players list:
        :param injured_batters list of inactive batters:
        :param roster json roster for the team:
        :return list of players that are neither hurt or had playing time during the game:
        """
        did_not_play_list = []
        players = roster["roster_all"]["queryResults"]["row"]
        for batter in injured_batters:
            player_list.remove(batter.full_name)

        for batter in game.batters_list:
            for player in player_list:
                if player == batter.full_name:
                    player_list.remove(player)

        for player in players:
            if "Active" in player["status_short"] and player["name_first_last"] in player_list:
                dnp = InactivePlayer(player["player_id"], player["name_first_last"], player["team_id"])
                dnp.position = player["position"]
                did_not_play_list.append(dnp)
                #player_list.remove(player["name_first_last"])
        return did_not_play_list


    def get_batters(self, boxscore, index):
        """
        :param boxscore: boxscore json
        :param index:  1 or 0 - opposite value of pitching index. If team bats first it has index of 0 and pitching is 1
        :return: list of batter objects
        """
        batters_list = []
        batters = boxscore["data"]["boxscore"]["batting"]
        for batter in batters[index]["batter"]:
            if batter["name_display_first_last"] in notable_batters or int(batter["hr"]) >= notable_batter_hr or \
                            int(batter["h"]) >= notable_batter_hits or int(batter["rbi"]) >= notable_batter_rbi:

                player = Batter(batter["id"], batter["name_display_first_last"], batter["name"])
                player.position = batter["pos"]
                player.at_bats = batter["ab"]
                player.hits = batter["h"]
                player.home_runs = batter["hr"]
                player.strikeouts = batter["so"]
                player.rbi = batter["rbi"]
                player.season_rbi = batter["s_rbi"]
                player.walks = batter["bb"]
                player.batting_average = batter["avg"]
                player.season_home_runs = batter["s_hr"]
                player.runs = batter["r"]
                player.doubles = batter["d"]
                player.triples = batter["t"]
                player.stolen_bases = batter["sb"]
                player._profile_url = self.get_player_profile_url(player.player_id, False,
                                                             datetime.datetime.now().strftime("%Y"))
                batters_list.append(player)
        return batters_list


    def set_pitcher_from_boxscore(self, current_pitcher, get_pitcher):
        if "name_display_first_last" in current_pitcher:
                try:
                    outs = int(current_pitcher["out"])
                    ip = outs / 3 + float((outs % 3) * .1)
                    if get_pitcher or current_pitcher["name_display_first_last"] in notable_pitchers or \
                                    ip >= notable_pitcher_innings or int(current_pitcher["so"]) >= notable_pitcher_strikeouts:

                        player = Pitcher(current_pitcher["id"], current_pitcher["name_display_first_last"],
                                         current_pitcher["name"])

                        player.position = current_pitcher["pos"]
                        player.wins = current_pitcher["w"]
                        player.losses = current_pitcher["l"]
                        player.innings_pitched = str(ip)
                        player.era = current_pitcher["era"]
                        player.earned_runs = current_pitcher["er"]
                        player.strikeouts = current_pitcher["so"]
                        player.hits = current_pitcher["h"]
                        player.walks = current_pitcher["bb"]
                        player.season_walks = current_pitcher["s_bb"]
                        player.season_strikeouts = current_pitcher["s_so"]
                        player.saves = current_pitcher["sv"]
                        player.holds = current_pitcher["hld"]
                        player._profile_url = self.get_player_profile_url(player.player_id, True,
                                                                     datetime.datetime.now().strftime("%Y"))

                        if "note" in current_pitcher:
                            player.note = current_pitcher["note"]

                        return player
                except Exception, e:
                    print
        return None


    def get_pitchers(self, boxscore, index, get_all_pitchers):
        """
        :param boxscore: boxscore json
        :param index: 1 or 0 - opposite value of batting index. If team bats first it has index of 0 and pitching is 1
        :return: list of pitcher objects
        """
        pitchers_list = []
        pitchers = boxscore["data"]["boxscore"]["pitching"]
        if "s_ip" in pitchers[index]["pitcher"] and "pos" in pitchers[index]["pitcher"]:
            try:
                player = self.set_pitcher_from_boxscore(pitchers[index]["pitcher"], get_all_pitchers)
                if player is not None:
                    pitchers_list.append(player)
            except Exception, e:
                print
        else:
            for p in pitchers[index]["pitcher"]:
                try:
                    player = self.set_pitcher_from_boxscore(p, get_all_pitchers)
                    if player is not None:
                        pitchers_list.append(player)
                except Exception, e:
                        print

        return pitchers_list


    def get_game_score_helper(self, game, game_data):
        current_inning = 0
        if "inning" in game_data:
            current_inning = game_data["inning"]

        if "linescore" in game_data and current_inning > 0:  #no linescore then game hasn't started
            game.set_team_ids(game_data["home_team_id"], game_data["away_team_id"])
            if "outs" in game_data:
                outs = self.get_inning_outs(game_data["outs"])
                runners = ""
                if "runner_on_base_status" in game_data:
                    runners = self.get_inning_runners(game_data["runner_on_base_status"])

                if "gameday_link" in game_data:
                    if len(game_data["gameday_link"]) > 0:
                        game.gameday_url = "http://www.milb.com/gameday/index.jsp?gid=%s&mode=gameday " %game_data["gameday_link"]

                game.inning_state = "\n###%s %s: %s - %s\n" % (game_data["inning_state"],
                                                               self.get_inning_suffix(game_data["inning"]), runners, outs)

                innings = game_data["linescore"]
                for inning in innings:
                    if "away_inning_runs" in inning and "home_inning_runs" in inning:
                        try:
                            game.set_inning_score(game.away_team_id, game.home_team_id, inning["inning"], inning["away_inning_runs"])
                            if "home_inning_runs" in inning:
                                game.set_inning_score(game.home_team_id, game.home_team_id, inning["inning"], inning["home_inning_runs"])

                        except Exception, e:
                            print
                    elif "away_inning_runs" in inning:
                        game.set_inning_score(game.away_team_id, game.home_team_id, innings["inning"], innings["away_inning_runs"])

                game.set_score(game.home_team_id, game.home_team_id, game_data["home_team_runs"])
                game.set_score(game.away_team_id, game.home_team_id, game_data["away_team_runs"])
                game.set_hits(game.home_team_id, game.home_team_id, game_data["home_team_hits"])
                game.set_hits(game.away_team_id, game.home_team_id, game_data["away_team_hits"])
                game.set_errors(game.home_team_id, game.home_team_id, game_data["home_team_errors"])
                game.set_errors(game.away_team_id, game.home_team_id, game_data["away_team_errors"])

                #sometimes the game data pulled isn't updated quickly, line score can set game data in this instance
                if "status" in game_data:
                    if game_data["status"].startswith("Final") or game_data["status"].startswith("Game Over"):
                        if len(game.result) == 0:
                            game.game_status = game_data["status"]
                            if game.home_score is not None:
                                if game.team_id == game.home_team_id:
                                    game.result = "W" if int(game.home_score) > int(game.away_score) else "L"
                                    game.game_finished = True
                                else:
                                    game.result = "W" if int(game.away_score) > int(game.home_score) else "L"
                                    game.game_finished = True
        return game


    def get_game_score(self, game, linescore):
        """
        :param game: game object
        :param linescore: linescore json
        :return: game object
        """
        if linescore is not None:
            if "game" in linescore["data"]:
                game_data = linescore["data"]["game"]
                return self.get_game_score_helper(game, game_data)
            else:
                game_data = linescore["data"]
                return self.get_game_score_helper(game, game_data)

        return game


    def get_player_profile_url(self, player_id, is_pitcher, season):
        url = "http://www.milb.com/player/index.jsp?sid=milb&player_id=" + player_id + "#/career/R/"
        if is_pitcher:
            url += "pitching/%s/ALL" % str(season)
        else:
            url += "batting/%s/ALL" % str(season)

        return url


    def get_team_profile_url(self, team_id):
        return "http://www.milb.com/index.jsp?sid=t" + str(team_id)


    def get_player_generic_profile(self, player_id):
        return "http://www.milb.com/player/index.jsp?sid=milb&player_id=" + player_id


    def get_inning_runners(self, runners):
        if int(runners) == 3:
            return "Runner on 3rd"
        elif int(runners) == 0:
            return "Bases Empty"
        elif int(runners) == 1:
            return "Runner on First"
        elif int(runners) == 2:
            return "Runner on Second"
        elif int(runners) == 4:
            return "Runners on First & Second"
        elif int(runners) == 5:
            return "Runners on First & Third"
        elif int(runners) == 6:
            return "Runners on Second & Third"
        elif int(runners) == 7:
            return "Bases Loaded"
        else:
            return ""


    def get_inning_outs(self, outs):
        if int(outs) > 1:
            return outs + " outs"
        else:
            return outs + " out"


    def get_inning_suffix(self, inning_number):
        if len(inning_number) > 0:
            number = int(inning_number)
            last_digit = number % 10
            if number / 10 == 1:
                    return inning_number + "th"
            else:
                if last_digit == 1:
                    return inning_number + "st"
                elif last_digit == 2:
                    return inning_number + "nd"
                elif last_digit == 3:
                    return inning_number + "rd"
                else:
                    return inning_number + "th"
        else:
            return ""


    def get_stats(self, team_ids, time_start, time_end):
        games_list = []
        batters_list = list(notable_batters)
        copy_batters_list = list(batters_list)
        pitchers_list = list(notable_pitchers)
        for team_id in team_ids:
            schedule = self.get_schedule(time_start, time_end, team_id, datetime.datetime.now().strftime("%Y"))
            if schedule is not None:
                games = self.get_games(schedule)
                for game in games:
                    roster = self.get_roster(game.team_id)
                    injured_batters = self.get_injury_list(batters_list, roster)
                    injured_pitchers = self.get_injury_list(pitchers_list, roster)
                    injuries = injured_batters + injured_pitchers
                    boxscore = self.get_boxscore(game)
                    linescore = self.get_linescore(game)
                    if boxscore is not None:   #check if there is a box score yet
                        self.get_game_score(game, linescore)
                        battingindex = 0 if boxscore["data"]["boxscore"]["home_id"] == team_id else 1
                        pitchingindex = 0 if battingindex == 1 else 1

                        game.reddit_text = redditpost.reddit_team_stats(game) + redditpost.reddit_score_table(game)
                        get_all_pitchers = "No Hitter" in game.game_status

                        if not game.game_status.startswith("Scheduled") and not game.game_status.startswith("Delayed Start"):
                            pitchers = self.get_pitchers(boxscore, pitchingindex, get_all_pitchers)
                            batters = self.get_batters(boxscore, battingindex)
                            for batter in batters:
                                batter.reddit_text = redditpost.reddit_batter_stats(batter)

                            for pitcher in pitchers:
                                pitcher.reddit_text = redditpost.reddit_pitcher_stats(pitcher)

                            for injury in injuries:
                                injury.reddit_text = redditpost.reddit_injury_stats(injury)

                            game.batters_list = batters
                            game.pitchers_list = pitchers
                            game.inactive_list = injuries

                            if game.game_finished:
                                did_not_play_list = self.get_did_not_play(game, copy_batters_list, injured_batters, roster)
                                for player in did_not_play_list:
                                    player.reddit_text = redditpost.reddit_did_not_play_stats(player)
                                game.day_off_list = did_not_play_list

                        games_list.append(game)
                    else:
                        game = self.get_game_score(game, linescore)
                        game.reddit_text = redditpost.reddit_team_stats(game) + redditpost.reddit_score_table(game)
                        games_list.append(game)

        return games_list
