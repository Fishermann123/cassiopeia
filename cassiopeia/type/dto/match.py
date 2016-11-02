import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm
    import sqlalchemy.orm.collections


@cassiopeia.type.core.common.inheritdocs
class MatchDetail(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        mapId (int): match map ID
        matchCreation (int): match creation time. Designates when the team select lobby is created and/or the match is made through match making, not when the game actually starts.
        matchDuration (int): match duration
        matchId (int): ID of the match
        matchMode (str): match mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        matchType (str): match type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        matchVersion (str): match version
        participantIdentities (list<ParticipantIdentity>): participant identity information
        participants (list<Participant>): participant information
        platformId (str): platform ID of the match
        queueType (str): match queue type (Legal values: CUSTOM, NORMAL_5x5_BLIND, RANKED_SOLO_5x5, RANKED_PREMADE_5x5, BOT_5x5, NORMAL_3x3, RANKED_PREMADE_3x3, NORMAL_5x5_DRAFT, ODIN_5x5_BLIND, ODIN_5x5_DRAFT, BOT_ODIN_5x5, BOT_5x5_INTRO, BOT_5x5_BEGINNER, BOT_5x5_INTERMEDIATE, RANKED_TEAM_3x3, RANKED_TEAM_5x5, BOT_TT_3x3, GROUP_FINDER_5x5, ARAM_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF_5x5, ONEFORALL_MIRRORMODE_5x5, BOT_URF_5x5, NIGHTMARE_BOT_5x5_RANK1, NIGHTMARE_BOT_5x5_RANK2, NIGHTMARE_BOT_5x5_RANK5, ASCENSION_5x5, HEXAKILL, KING_PORO_5x5, COUNTER_PICK)
        region (str): region where the match was played
        season (str): season match was played (Legal values: PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015)
        teams (list<Team>): team information
        timeline (Timeline): match timeline data (not included by default)
    """
    def __init__(self, dictionary):
##        self.mapId = dictionary.get("mapId", 0)
##        self.matchCreation = dictionary.get("matchCreation", 0)
##        self.matchDuration = dictionary.get("matchDuration", 0)
        self.matchId = dictionary.get("matchId", 0)
##        self.matchMode = dictionary.get("matchMode", "")
##        self.matchType = dictionary.get("matchType", "")
##        self.matchVersion = dictionary.get("matchVersion", "")
        self.participantIdentities = [(ParticipantIdentity(pi) if not isinstance(pi, ParticipantIdentity) else pi) for pi in dictionary.get("participantIdentities", []) if pi]
        self.participants = [(Participant(p) if not isinstance(p, Participant) else p) for p in dictionary.get("participants", []) if p]
##        self.platformId = dictionary.get("platformId", "")
##        self.queueType = dictionary.get("queueType", "")
##        self.region = dictionary.get("region", "")
##        self.season = dictionary.get("season", "")
        #self.teams = [(Team(t) if not isinstance(t, Team) else t) for t in dictionary.get("teams", []) if t]
        val = dictionary.get("timeline", None)
        self.timeline = Timeline(val) if val and not isinstance(val, Timeline) else val


    @property
    def summoner_ids(self):
        """
        Gets all item IDs contained in this object
        """
        ids = set()
        for p in self.participantIdentities:
            if p.player and p.player.summonerId:
                ids.add(p.player.summonerId)
        return ids


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all item IDs contained in this object
    """
    def __init__(self, dictionary):
##        self.championId = dictionary.get("championId", 0)
##        self.highestAchievedSeasonTier = dictionary.get("highestAchievedSeasonTier", "")
##        self.masteries = [(Mastery(m) if not isinstance(m, Mastery) else m) for m in dictionary.get("masteries", []) if m]
        self.participantId = dictionary.get("participantId", 0)
##        self.runes = [(Rune(r) if not isinstance(r, Rune) else r) for r in dictionary.get("runes", []) if r]
##        self.spell1Id = dictionary.get("spell1Id", 0)
##        self.spell2Id = dictionary.get("spell2Id", 0)
        val = dictionary.get("stats", None)
        self.stats = ParticipantStats(val) if val and not isinstance(val, ParticipantStats) else val
        self.teamId = dictionary.get("teamId", 0)
        val = dictionary.get("timeline", None)
        self.timeline = ParticipantTimeline(val) if val and not isinstance(val, ParticipantTimeline) else val


@cassiopeia.type.core.common.inheritdocs
class ParticipantIdentity(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all champion IDs contained in this object
    """
    def __init__(self, dictionary):
        self.participantId = dictionary.get("participantId", 0)
        val = dictionary.get("player", None)
        self.player = Player(val) if val and not isinstance(val, Player) else val


@cassiopeia.type.core.common.inheritdocs
class ParticipantStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all summoner spell IDs contained in this object
    """
    def __init__(self, dictionary):
        self.champLevel = dictionary.get("champLevel", 0)
        self.winner = dictionary.get("winner", False)


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimeline(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        championId (int): champion ID
        highestAchievedSeasonTier (str): highest ranked tier achieved for the previous season, if any, otherwise null. Used to display border in game loading screen. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, UNRANKED)
        masteries (list<Mastery>): list of mastery information
        participantId (int): participant ID
        runes (list<Rune>): list of rune information
        spell1Id (int): first summoner spell ID
        spell2Id (int): second summoner spell ID
        stats (ParticipantStats): participant statistics
        teamId (int): team ID
        timeline (ParticipantTimeline): timeline data. Delta fields refer to values for the specified period (e.g., the gold per minute over the first 10 minutes of the game versus the second 20 minutes of the game. Diffs fields refer to the deltas versus the calculated lane opponent(s).
    """
    def __init__(self, dictionary):
        self.lane = dictionary.get("lane", "")
        self.role = dictionary.get("role", "")



@cassiopeia.type.core.common.inheritdocs
class Player(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        bans (list<BannedChampion>): if game was draft mode, contains banned champion data, otherwise null
        baronKills (int): number of times the team killed baron
        dominionVictoryScore (int): if game was a dominion game, specifies the points the team had at game end, otherwise null
        dragonKills (int): number of times the team killed dragon
        firstBaron (bool): flag indicating whether or not the team got the first baron kill
        firstBlood (bool): flag indicating whether or not the team got first blood
        firstDragon (bool): flag indicating whether or not the team got the first dragon kill
        firstInhibitor (bool): flag indicating whether or not the team destroyed the first inhibitor
        firstRiftHerald (bool): flag indicating whether or not the team got the first rift herald kill
        firstTower (bool): flag indicating whether or not the team destroyed the first tower
        inhibitorKills (int): number of inhibitors the team destroyed
        riftHeraldKills (int): number of times the team killed rift herald
        teamId (int): team ID
        towerKills (int): number of towers the team destroyed
        vilemawKills (int): number of times the team killed vilemaw
        winner (bool): flag indicating whether or not the team won
    """
    def __init__(self, dictionary):
        #self.matchHistoryUri = dictionary.get("matchHistoryUri", "")
        #self.profileIcon = dictionary.get("profileIcon", 0)
        self.summonerId = dictionary.get("summonerId", 0)
        #self.summonerName = dictionary.get("summonerName", "")




###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_match_detail():
    global MatchDetail

    @cassiopeia.type.core.common.inheritdocs
    class MatchDetail(MatchDetail, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchDetail"
        #mapId = sqlalchemy.Column(sqlalchemy.Integer)
        #matchCreation = sqlalchemy.Column(sqlalchemy.BigInteger)
        #matchDuration = sqlalchemy.Column(sqlalchemy.Integer)
        matchId = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
        #matchMode = sqlalchemy.Column(sqlalchemy.String(30))
        #matchType = sqlalchemy.Column(sqlalchemy.String(30))
        #matchVersion = sqlalchemy.Column(sqlalchemy.String(30))
        participantIdentities = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantIdentity", cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Participant", cascade="all, delete-orphan", passive_deletes=True)
        #platformId = sqlalchemy.Column(sqlalchemy.String(30))
        #queueType = sqlalchemy.Column(sqlalchemy.String(30))
        #region = sqlalchemy.Column(sqlalchemy.String(30))
        #season = sqlalchemy.Column(sqlalchemy.String(30))
        #teams = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Team", cascade="all, delete-orphan", passive_deletes=True)
        #timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Timeline", uselist=False, cascade="all, delete-orphan", passive_deletes=True)


def _sa_bind_participant():
    global Participant

    @cassiopeia.type.core.common.inheritdocs
    class Participant(Participant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipant"
        #championId = sqlalchemy.Column(sqlalchemy.Integer)
        #highestAchievedSeasonTier = sqlalchemy.Column(sqlalchemy.String(30))
        #masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Mastery", cascade="all, delete-orphan", passive_deletes=True)
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        #runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Rune", cascade="all, delete-orphan", passive_deletes=True)
        #spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        #spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimeline", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))


def _sa_bind_participant_identity():
    global ParticipantIdentity

    @cassiopeia.type.core.common.inheritdocs
    class ParticipantIdentity(ParticipantIdentity, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantIdentity"
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        player = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Player", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))


def _sa_bind_participant_stats():
    global ParticipantStats

    @cassiopeia.type.core.common.inheritdocs
    class ParticipantStats(ParticipantStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantStats"
        champLevel = sqlalchemy.Column(sqlalchemy.Integer)
        winner = sqlalchemy.Column(sqlalchemy.Boolean)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))


def _sa_bind_participant_timeline():
    global ParticipantTimeline

    @cassiopeia.type.core.common.inheritdocs
    class ParticipantTimeline(ParticipantTimeline, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantTimeline"
        lane = sqlalchemy.Column(sqlalchemy.String(30))
        role = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))


def _sa_bind_player():
    global Player

    @cassiopeia.type.core.common.inheritdocs
    class Player(Player, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchPlayer"
        #matchHistoryUri = sqlalchemy.Column(sqlalchemy.String(50))
        #profileIcon = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        #summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantIdentity._id", ondelete="CASCADE"))



def _sa_bind_all():
    _sa_bind_match_detail()
    _sa_bind_participant()
    _sa_bind_participant_identity()
    #_sa_bind_team()
    #_sa_bind_timeline()
    #_sa_bind_mastery()
    _sa_bind_participant_stats()
    _sa_bind_participant_timeline()
    #_sa_bind_rune()
    _sa_bind_player()
    #_sa_bind_banned_champion()
    #_sa_bind_frame()
    #_sa_bind_participant_timeline_data()
    #_sa_bind_event()
    #_sa_bind_participant_frame()
    #_sa_bind_position()
