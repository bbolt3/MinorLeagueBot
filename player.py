class Batter(object):

    def __init__(self, player_id, full_name, name):
        self.full_name = full_name
        self.name = name
        self.player_id = player_id
        self._at_bats = None
        self._batting_average = None
        self._doubles = None
        self._hits = None
        self._home_runs = None
        self._triples = None
        self._strikeouts = None
        self._walks = None
        self._season_home_runs = None
        self._season_rbi = None
        self._rbi = None
        self._runs = None
        self._profile_url = None
        self._position = None
        self._stolen_bases = None
        self._reddit_text = None

    @property
    def at_bats(self):
        return self._at_bats

    @at_bats.setter
    def at_bats(self, value):
        self._at_bats = value

    @property
    def hits(self):
        return self._hits

    @hits.setter
    def hits(self, value):
        self._hits = value

    @property
    def home_runs(self):
        return self._home_runs

    @home_runs.setter
    def home_runs(self, value):
        self._home_runs = value

    @property
    def strikeouts(self):
        return self._strikeouts

    @strikeouts.setter
    def strikeouts(self, value):
        self._strikeouts = value

    @property
    def walks(self):
        return self._walks

    @walks.setter
    def walks(self, value):
        self._walks = value

    @property
    def rbi(self):
        return self._rbi

    @rbi.setter
    def rbi(self, value):
        self._rbi = value

    @property
    def batting_average(self):
        return self._batting_average

    @batting_average.setter
    def batting_average(self, value):
        self._batting_average = value

    @property
    def season_home_runs(self):
        return self._season_home_runs

    @season_home_runs.setter
    def season_home_runs(self, value):
        self._season_home_runs = value

    @property
    def season_rbi(self):
        return self._season_rbi

    @season_rbi.setter
    def season_rbi(self, value):
        self._season_rbi = value

    @property
    def runs(self):
        return self._runs

    @runs.setter
    def runs(self, value):
        self._runs = value

    @property
    def doubles(self):
        return self._doubles

    @doubles.setter
    def doubles(self, value):
        self._doubles = value

    @property
    def triples(self):
        return self._triples

    @triples.setter
    def triples(self, value):
        self._triples = value

    @property
    def profile_url(self):
        return self._profile_url

    @profile_url.setter
    def profile_url(self, value):
        self._profile_url = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def stolen_bases(self):
        return self._stolen_bases

    @stolen_bases.setter
    def stolen_bases(self, value):
        self._stolen_bases = value

    @property
    def reddit_text(self):
        return self._reddit_text

    @reddit_text.setter
    def reddit_text(self, value):
        self._reddit_text = value


class Pitcher(object):

    def __init__(self, player_id, full_name, name):
        self.player_id = player_id
        self.full_name = full_name
        self.name = name
        self._wins = None
        self._earned_runs = None
        self._era = None
        self._holds = None
        self._hits = None
        self._note = None
        self._losses = None
        self._innings_pitched = None
        self._strikeouts = None
        self._walks = None
        self._season_strikeouts = None
        self._season_walks = None
        self._saves = None
        self._profile_url = None
        self._position = None
        self._reddit_text = None

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def innings_pitched(self):
        return self._innings_pitched

    @innings_pitched.setter
    def innings_pitched(self, value):
        self._innings_pitched = value

    @property
    def era(self):
        return self._era

    @era.setter
    def era(self, value):
        self._era = value

    @property
    def earned_runs(self):
        return self._earned_runs

    @earned_runs.setter
    def earned_runs(self, value):
        self._earned_runs = value

    @property
    def hits(self):
        return self._hits

    @hits.setter
    def hits(self, value):
        self._hits = value

    @property
    def strikeouts(self):
        return self._strikeouts

    @strikeouts.setter
    def strikeouts(self, value):
        self._strikeouts = value

    @property
    def season_strikeouts(self):
        return self._season_strikeouts

    @season_strikeouts.setter
    def season_strikeouts(self, value):
        self._season_strikeouts = value

    @property
    def walks(self):
        return self._walks

    @walks.setter
    def walks(self, value):
        self._walks = value

    @property
    def season_walks(self):
        return self._season_walks

    @season_walks.setter
    def season_walks(self, value):
        self._season_walks = value

    @property
    def saves(self):
        return self._saves

    @saves.setter
    def saves(self, value):
        self._saves = value

    @property
    def holds(self):
        return self._holds

    @holds.setter
    def holds(self, value):
        self._holds = value

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value

    @property
    def profile_url(self):
        return self._profile_url

    @profile_url.setter
    def profile_url(self, value):
        self._profile_url = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def reddit_text(self):
        return self._reddit_text

    @reddit_text.setter
    def reddit_text(self, value):
        self._reddit_text = value
