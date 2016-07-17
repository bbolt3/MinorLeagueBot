class Game(object):

    def __init__(self, team_id, team_name, game_id, home_team_name, away_team_name, home_time, local_timezone, location):
        self.home_score_innings = {}
        self.away_score_innings = {}
        self._batters_list = []
        self._pitchers_list = []
        self._inactive_list = []
        self._day_off_list = []
        self.team_id = team_id
        self.team_name = team_name
        self.game_id = game_id
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.home_time = home_time
        self.timezone = local_timezone
        self.location = location
        self.home_team_id = None
        self.away_team_id = None
        self.home_score = None
        self.away_score = None
        self.away_team_hits = None
        self.home_team_hits = None
        self.home_team_errors = None
        self.away_team_errors = None
        self._result = None
        self._team_record = None
        self._game_status = None
        self._scheduled_start = None
        self._team_local_timezone = None
        self._game_number = None
        self._double_header = None
        self._inning_state = None
        self._listen = None
        self._opponent_name_full = None
        self._opponent_record = None
        self._reddit_text = None
        self._game_finished = None
        self._gameday_url = None
        self._ignore_schedule = None
        self._division_code = None
        self._start_time_edt = None

    def set_inning_score(self, team_id, home_team_id, inning, runs):
        self.home_team_id = home_team_id
        if team_id == home_team_id:
            self.home_score_innings[inning] = runs
        else:
            self.away_score_innings[inning] = runs

    def set_score(self, team_id, home_team_id, score):
        self.home_team_id = home_team_id
        if team_id == home_team_id:
            self.home_score = score
        else:
            self.away_score = score

    def set_hits(self, team_id, home_team_id, hits):
        self.home_team_id = home_team_id
        if team_id == home_team_id:
            self.home_team_hits = hits
        else:
            self.away_team_hits = hits

    def set_errors(self, team_id, home_team_id, errors):
        self.home_team_id = home_team_id
        if team_id == home_team_id:
            self.home_team_errors = errors
        else:
            self.away_team_errors = errors

    def set_team_ids(self, home_team, away_team):
        self.home_team_id = home_team
        self.away_team_id = away_team

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def team_record(self):
        return self._team_record

    @team_record.setter
    def team_record(self, value):
        self._team_record = value

    @property
    def game_status(self):
        return self._game_status

    @game_status.setter
    def game_status(self, value):
        self._game_status = value

    @property
    def scheduled_start(self):
        return self._scheduled_start

    @scheduled_start.setter
    def scheduled_start(self, value):
        self._scheduled_start = value

    @property
    def team_local_timezone(self):
        return self._team_local_timezone

    @team_local_timezone.setter
    def team_local_timezone(self, value):
        self._team_local_timezone = value

    @property
    def double_header(self):
        return self._double_header

    @double_header.setter
    def double_header(self, value):
        self._double_header = value

    @property
    def game_number(self):
        return self._game_number

    @game_number.setter
    def game_number(self, value):
        self._game_number = value

    @property
    def inning_state(self):
        return self._inning_state

    @inning_state.setter
    def inning_state(self, value):
        self._inning_state = value

    @property
    def listen(self):
        return self._listen

    @listen.setter
    def listen(self, value):
        self._listen = value

    @property
    def opponent_name_full(self):
        return self._opponent_name_full

    @opponent_name_full.setter
    def opponent_name_full(self, value):
        self._opponent_name_full = value

    @property
    def opponent_record(self):
        return self._opponent_record

    @opponent_record.setter
    def opponent_record(self, value):
        self._opponent_record = value

    @property
    def batters_list(self):
        return self._batters_list

    @batters_list.setter
    def batters_list(self, value):
        self._batters_list = value

    @property
    def pitchers_list(self):
        return self._pitchers_list

    @pitchers_list.setter
    def pitchers_list(self, value):
        self._pitchers_list = value

    @property
    def inactive_list(self):
        return self._inactive_list

    @inactive_list.setter
    def inactive_list(self, value):
        self._inactive_list = value

    @property
    def day_off_list(self):
        return self._day_off_list

    @day_off_list.setter
    def day_off_list(self, value):
        self._day_off_list = value

    @property
    def reddit_text(self):
        return self._reddit_text

    @reddit_text.setter
    def reddit_text(self, value):
        self._reddit_text = value

    @property
    def game_finished(self):
        return self._game_finished

    @game_finished.setter
    def game_finished(self, value):
        self._game_finished = value

    @property
    def gameday_url(self):
        return self._gameday_url

    @gameday_url.setter
    def gameday_url(self, value):
        self._gameday_url = value

    @property
    def ignore_schedule(self):
        return self._ignore_schedule

    @ignore_schedule.setter
    def ignore_schedule(self, value):
        self._ignore_schedule = value

    @property
    def division_code(self):
        return self._division_code

    @division_code.setter
    def division_code(self, value):
        self._division_code = value

    @property
    def start_time_edt(self):
        return self._start_time_edt

    @start_time_edt.setter
    def start_time_edt(self, value):
        self._start_time_edt = value