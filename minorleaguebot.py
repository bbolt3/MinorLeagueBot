import datetime
import milbdata
from watchlist import *
from redditpost import reddit_brief_text_post, reddit_list_players

def main():
    #if time start or end are a value any time during a day, then that day is returned. Use hours to offset time
    hours = 6
    #teams = [team_aaa_id, team_aa_id, team_higha_id, team_lowa_id, team_shortseason_id, team_azl_id, team_dsl_id, team_dsl2_id]
    teams = [team1, team2, team3, team4, team5, team6, team7, team8]
    subject = "Cubs Minor League Stats %s/%s" % (str(datetime.datetime.now().month),
                                                 str((datetime.datetime.now() - datetime.timedelta(hours=hours)).day))

    milb_stats = milbdata.MilbData()

    datetime_now = datetime.datetime.now()
    time_start = milb_stats.date_format(datetime_now - milbdata.datetime.timedelta(hours=hours))
    #time_start = milb_stats.date_format(datetime_now + milbdata.datetime.timedelta(hours=hours))
    #time_end = date_format(datetime_now + datetime.timedelta(hours=16))

    reddit_brief_text_post(teams, time_start, time_start, subject, milb_stats)
    #print reddit_list_players(notable_batters)
    #print reddit_list_players(notable_pitchers)



if __name__ == '__main__':
    main()
