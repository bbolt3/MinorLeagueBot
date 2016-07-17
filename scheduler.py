import pytz
import datetime
import sys

def next_game_update(games, update_interval):
    central = pytz.timezone('US/Central')
    eastern = pytz.timezone("US/Eastern")
    soonest = sys.maxint
    double_headers = {}
    for game in games:
        if (not game.game_finished) and (not game.ignore_schedule):
            if game.double_header == 'Y':
                if game.team_id in double_headers:
                    double_headers[game.team_id] += int(game.game_number)
                else:
                    double_headers[game.team_id] = int(game.game_number)

            target_dt = eastern.localize(game.start_time_edt).astimezone(central)
            local_time = central.normalize(target_dt)
            dt = datetime.datetime.now(central)
            time_diff = (local_time - dt).total_seconds()
            if (time_diff < 900 and game.team_id not in double_headers) or (game.team_id in double_headers and ((double_headers[game.team_id] == 1 and time_diff < 900) or double_headers[game.team_id] == 2)):
                return update_interval
            elif time_diff > 0:
                if (game.team_id not in double_headers) or (game.team_id in double_headers and double_headers[game.team_id] < 3):
                    if soonest > time_diff - 900:
                        soonest = time_diff - 900

    if soonest == sys.maxint:
        soonest = 3600
    elif soonest < 0:
        soonest = update_interval
    return soonest
