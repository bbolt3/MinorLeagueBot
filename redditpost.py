import praw
import time
from milbdata import *
from redditlogin import *

networkdata = None


class RedditPost(object):
     def __init__(self, title, post_subreddit, url, post_id):
         self.title = title
         self.post_subreddit = post_subreddit
         self.url = url
         self.post_id = post_id


def reddit_score_table(game):
    """
    :param game:  game object
    :return: string of a table of linescore to post on reddit
    """
    table = ""
    innings = len(game.away_score_innings)
    if int(innings) >= 1:
        table = "Team|"
        #innings + r + h + e
        for i in range(1, innings + 1):
            table += str(i) + "|"
        table += "R|H|E|"
        #cell alignments
        table += "\n:--|"
        for i in range(1, innings + 1):
            table += ":--|"
        table += "--:|--:|--:|"
        #away team
        table += "\n%s|" % game.away_team_name
        for i in range(1, innings + 1):
            table += game.away_score_innings[str(i)] + "|"
        #print r h e
        table += "%s|%s|%s|" % (game.away_score, game.away_team_hits, game.away_team_errors)
        #home team
        table += "\n%s|" % game.home_team_name
        for i in range(1, innings + 1):
            if len(game.home_score_innings) >= innings:
                home_inning = "X" if len(game.home_score_innings[str(i)]) == 0 and game.game_status.startswith("Final") or \
                    len(game.home_score_innings[str(i)]) == 0 and game.game_status.startswith("Game Over") else \
                    game.home_score_innings[str(i)]
            else:
                home_inning = ""

            table += home_inning + "|"
        table += "%s|%s|%s\n" % (game.home_score, game.home_team_hits, game.home_team_errors)
    return table


def reddit_team_stats(game):
    team_stats = "---  \n#[%s](%s)" % (game.team_name, networkdata.get_team_profile_url(game.team_id))
    team_stats += "(%s) vs. %s(%s) \n###Status: " % (game.team_record, game.opponent_name_full, game.opponent_record)
    if game.result is not None:
        if game.game_status.startswith("Final") or game.game_status.startswith("Game Over") or game.result == "L" \
                or game.result == "W":
            if game.double_header == "Y":
                team_stats += " Lost Game #" + game.game_number if game.result == "L" else " Won Game #" + game.game_number
                game.game_finished = True
            else:
                team_stats += " Lost Game" if game.result == "L" else " Won Game"
                game.game_finished = True

            if game.away_team_hits is not None and game.team_id is not None and game.home_team_hits is not None and \
                            game.away_team_id is not None and int(game.away_team_hits) == 0 and \
                            len(game.home_team_hits) > 0 and len(game.away_team_hits) > 0 and \
                            game.team_id == game.home_team_id or int(game.home_team_hits) == 0 and \
                            game.team_id == game.away_team_id:
                game.game_status += " No Hitter"
                team_stats += " (No Hitter)"
        elif game.game_status.startswith("Scheduled"):
            if int(game.game_number) == 1:
                team_stats += " %s %s %s" % (game.game_status, game._scheduled_start, game._team_local_timezone)
            elif game.double_header == "Y" and int(game.game_number) > 1:
                team_stats += " %s Game #%s" % (game.game_status, game.game_number)
        elif "Warmup" in game.game_status:
            if len(game.away_score_innings) > 0:
                game.game_status = "In Progress" #for some reason game starts but remains in warmup state for ~3 innings
                team_stats += " %s " % game.game_status
                if game.gameday_url is not None:
                    if len(game.gameday_url) > 0:
                        team_stats += "([Gameday](%s))" % game.gameday_url
                if game.listen is not None:
                    if len(game.listen) > 0:
                        team_stats += "([Listen via TuneIn](%s)) " % game.listen

                team_stats += " %s" % game.inning_state
            else:
                team_stats += " " + game.game_status
        elif "In Progress" in game.game_status:
            team_stats += " %s " % game.game_status
            if game.gameday_url is not None:
                if len(game.gameday_url) > 0:
                    team_stats += "([Gameday](%s))" % game.gameday_url
            if game.listen is not None:
                if len(game.listen) > 0:
                    team_stats += "([Listen via TuneIn](%s)) " % game.listen

            team_stats += " %s" % game.inning_state
        elif "Postponed" in game.game_status or "Suspended" in game.game_status or "Cancelled" in game.game_status:
            team_stats += " " + game.game_status
            game.game_finished = True
        else:
            team_stats += " " + game.game_status

    return team_stats +"\n"


def reddit_batter_stats(batter):
    if batter.at_bats == "0" and batter.hits == "0" and batter.walks == "0" and batter.rbi == "0"  \
            and batter.runs == "0":
        return ""

    batter_stats = "%s [%s](%s): " % (batter.position, batter.full_name, batter.profile_url)
    batter_stats += " %s-%s " % (batter.hits, batter.at_bats)
    batter_stats += batter.batting_average + " AVG"
    if int(batter.home_runs) > 0:
        batter_stats += ", %s HR(%s)" % (batter.home_runs, batter.season_home_runs)
    if int(batter.triples) > 0:
        if int(batter.triples) > 1:
            batter_stats += ", %s 3B" % batter.triples
        else:
            batter_stats += ", 3B"
    if int(batter.doubles) > 0:
        if int(batter.doubles) > 1:
            batter_stats += ", %s 2B" % batter.doubles
        else:
            batter_stats += ", 2B"
    if int(batter.rbi) > 0:
        batter_stats += ", %s RBI(%s)" % (batter.rbi, batter.season_rbi)
    if int(batter.strikeouts) > 0:
        batter_stats += ", %sK" % batter.strikeouts
    if int(batter.walks) > 0:
        batter_stats += ", %sBB" % batter.walks
    if int(batter.stolen_bases) > 0:
        batter_stats += ", %s SB" % batter.stolen_bases

    return batter_stats + "\n\n"


def reddit_pitcher_stats(pitcher):
    if pitcher.innings_pitched == "0.0" and pitcher.walks == "0" and pitcher.strikeouts == "0" and  \
            pitcher.earned_runs == "0" and pitcher.hits == "0":
        return ""
    pitcher_stats = "%s [%s](%s): " % (pitcher.position, pitcher.full_name, pitcher.profile_url)
    if pitcher.note is not None:
        pitcher_stats += pitcher.note + " "
    pitcher_stats += pitcher.innings_pitched + "IP, "
    pitcher_stats += "%s ER (%s ERA) " % (pitcher.earned_runs, pitcher.era)
    pitcher_stats += pitcher.hits + "H "
    pitcher_stats += pitcher.walks + "BB "
    pitcher_stats += pitcher.strikeouts + "K "

    return pitcher_stats + "\n\n"


def reddit_did_not_play_stats(player):
    url = networkdata.get_player_generic_profile(player.player_id)
    return "\n*%s [%s](%s)*\n\n" % (player.position, player.full_name, url)


def reddit_injury_stats(injured_player):
    url = networkdata.get_player_generic_profile(injured_player.player_id)
    return "\n*%s [%s](%s) - Status: %s*\n\n" % (injured_player.position, injured_player.full_name, url,
                                                 injured_player.injury)


def reddit_post_brief_box_score(game):
    output = ""
    if len(game.batters_list) > 0:
        for batter in game.batters_list:
            output += batter.reddit_text
    if len(game.pitchers_list) > 0:
        for pitcher in game.pitchers_list:
            output += pitcher.reddit_text
    if game.game_finished:
        if len(game.day_off_list) > 0:
            output += "\n\n###Did Not Play\n\n"
            for player in game.day_off_list:
                output += player.reddit_text
    if len(game.inactive_list) > 0:
        output += "\n\n###Inactive Players on Roster\n\n"
        for inactive in game.inactive_list:
            output += inactive.reddit_text

    return output


def reddit_brief_text_post(teams, time_start, time_end, post_title, milb_data):
    global networkdata
    networkdata = milb_data
    is_finished = False
    post = None
    while not is_finished:
        games = networkdata.get_stats(teams, time_start, time_end)
        output = ""
        games_finished = 0
        for game in games:
            output += game.reddit_text
            output += reddit_post_brief_box_score(game)

            if game.game_finished:
                games_finished += 1
            if games_finished == len(games):
                is_finished = True

        if len(games) > 0 and len(output) > 0:
            try:
                reddit = praw.Reddit(user_agent=useragent)
                reddit.login(username=user, password=password, disable_warning=True)
                if reddit is not None:
                    if post is None:
                        submission = reddit_check_post_exists(post_title)
                        if submission is None:
                            try:
                                post = reddit.submit(subreddit, post_title, text=output)
                                print "New post:%s" % post.url
                            except Exception, e:
                                print e.message
                        else:
                            try:
                                post = reddit.get_submission(submission_id=submission.post_id)
                                post = post.edit(output)
                                print "updated post:%s" % post.url
                            except Exception, e:
                                print e.message
                    else:
                        try:
                            post = post.edit(output)
                            print "updated post:%s" % post.url
                        except Exception, e:
                            print e.message
            except:
                print
        if not is_finished:
            print "updating in %s minutes" % str(time_to_wait / 60)
            time.sleep(time_to_wait)

    print "All games have completed. Finished."


def reddit_check_post_exists(title):
    reddit = praw.Reddit(user_agent=useragent)
    posts = reddit_get_past_five_submissions(reddit)
    for post in posts:
        if str(post.title).lower() == title.lower() and str(post.post_subreddit).lower() == subreddit.lower():
            return post
    return None


def reddit_get_past_five_submissions(reddit):
    submissions = []
    reddit_user = reddit.get_redditor(user)
    posts = reddit_user.get_submitted()
    counter = 1
    for post in posts:
        reddit_post = RedditPost(post.title, post.subreddit, post.url, post.id)
        submissions.append(reddit_post)
        counter += 1
        if counter > 5:
            break

    return submissions


def reddit_list_players(player_list):
    output = ""
    for player in player_list:
        output += "* %s\n" % player
    return output