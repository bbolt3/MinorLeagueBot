class InactivePlayer(object):

    def __init__(self, player_id, full_name, team_id):
        self.player_id = player_id
        self.full_name = full_name
        self.team_id = team_id
        self._injury = None
        self._injury_date = None
        self._reddit_text = None
        self._position = None

    @property
    def injury(self):
        return self._injury

    @injury.setter
    def injury(self, value):
        self._injury = value

    @property
    def injury_date(self):
        return self._injury_date

    @injury_date.setter
    def injury_date(self, value):
        self._injury_date = value

    @property
    def reddit_text(self):
        return self._reddit_text

    @reddit_text.setter
    def reddit_text(self, value):
        self._reddit_text = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value