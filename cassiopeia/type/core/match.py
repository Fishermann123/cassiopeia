import datetime

import cassiopeia.riotapi
import cassiopeia.type.dto.common
import cassiopeia.type.core.common
import cassiopeia.type.dto.match

try:
    from future.builtins.misc import super
except ImportError:
    pass


@cassiopeia.type.core.common.inheritdocs
class Match(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.MatchDetail

    def __str__(self):
        return "Match #{id}".format(id=self.id)

    def __iter__(self):
        return iter(self.participants)

    def __len__(self):
        return len(self.participants)

    def __getitem__(self, index):
        return self.participants[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def map(self):
        """
        Returns:
            Map: the map the match was played on
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """
        Returns:
            datetime: when the match was created
        """
        return datetime.datetime.utcfromtimestamp(self.data.matchCreation / 1000) if self.data.matchCreation else None

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        """
        Returns:
            datetime: duration of the match
        """
        return datetime.timedelta(seconds=self.data.matchDuration)

    @property
    def id(self):
        """
        Returns:
            int: the match ID
        """
        return self.data.matchId

    @property
    def mode(self):
        """
        Returns:
            GameMode: the game mode
        """
        return cassiopeia.type.core.common.GameMode(self.data.matchMode) if self.data.matchMode else None

    @property
    def type(self):
        """
        Returns:
            GameType: the game type
        """
        return cassiopeia.type.core.common.GameType(self.data.matchType) if self.data.matchType else None

    @property
    def version(self):
        """
        Returns:
            str: the patch this match was played in
        """
        return self.data.matchVersion

    @cassiopeia.type.core.common.lazyproperty
    #@cassiopeia.type.core.common.indexable([("summoner_name", str), ("summoner_id", int), ("champion.name", str), ("champion.id", int), ("champion", cassiopeia.type.core.staticdata.Champion), ("summoner", cassiopeia.type.core.summoner.Summoner)])
    def participants(self):
        """
        Returns:
            list<Participant>: the participants in this match
        """
        participants = []
        for i in range(len(self.data.participants)):
            p = CombinedParticipant(self.data.participants[i], self.data.participantIdentities[i])
            participants.append(Participant(p))
        return sorted(participants, key=lambda p: p.id)

    @property
    def platform(self):
        """
        Returns:
            Platform: the platform (ie server) for this match
        """
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

    @property
    def queue(self):
        """
        Returns:
            Queue: the queue type for this match
        """
        return cassiopeia.type.core.common.Queue(self.data.queueType) if self.data.queueType else None

    @property
    def region(self):
        """
        Returns:
            Region: the region the match was played in
        """
        return cassiopeia.type.core.common.Region(self.data.region.lower()) if self.data.region else None

    @property
    def season(self):
        """
        Returns:
            Season: the season this match was played in
        """
        return cassiopeia.type.core.common.Season(self.data.season) if self.data.season else None




@cassiopeia.type.core.common.inheritdocs
class CombinedParticipant(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, participant, identity):
        self.participant = participant
        self.identity = identity


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = CombinedParticipant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner_name, champ=self.champion)

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion this participant played
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.participant.championId) if self.data.participant.championId else None

    @property
    def previous_season_tier(self):
        """
        Returns:
            Tier: the participant's tier last season
        """
        return cassiopeia.type.core.common.Tier(self.data.participant.highestAchievedSeasonTier) if self.data.participant.highestAchievedSeasonTier else None


    @property
    def id(self):
        """
        Returns:
            int: the participant ID
        """
        return self.data.participant.participantId


    @property
    def summoner_spell_d(self):
        """
        Returns:
            SummonerSpell: the participant's first summoner spell
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell1Id) if self.data.participant.spell1Id else None

    @property
    def summoner_spell_f(self):
        """
        Returns:
            SummonerSpell: the participant's second summoner spell
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell2Id) if self.data.participant.spell2Id else None

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            ParticipantStats: the participant's stats
        """
        return ParticipantStats(self.data.participant.stats) if self.data.participant.stats else None

    @property
    def side(self):
        """
        Returns:
            Side: the side this participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.participant.teamId) if self.data.participant.teamId else None


    @property
    def match_history_uri(self):
        """
        Returns:
            str: the the URI to access this player's match history online
        """
        return self.data.identity.player.matchHistoryUri if self.data.identity.player else None

    @property
    def summoner(self):
        """
        Returns:
            Summoner: the summoner associated with this participant
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.identity.player.summonerId) if self.data.identity.player and self.data.identity.player.summonerId else None

    @property
    def summoner_id(self):
        """
        Returns:
            str: the participant's summoner id
        """
        return self.data.identity.player.summonerId if self.data.identity.player else None

    @property
    def summoner_name(self):
        """
        Returns:
            str: the participant's summoner name
        """
        return self.data.identity.player.summonerName if self.data.identity.player else None





@cassiopeia.type.core.common.inheritdocs
class ParticipantStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantStats

    def __str__(self):
        return "Participant Stats"

    @property
    def kda(self):
        """
        Returns:
            float: the participant's kda
        """
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        """
        Returns:
            int: the total number of assists this participant had
        """
        return self.data.assists

    @property
    def champion_level(self):
        """
        Returns:
            int: the champion level of the participant when the game ended
        """
        return self.data.champLevel

    @property
    def combat_score(self):
        """
        Returns:
            int: dominion only. the part of the participant's score that came from combat-related activities
        """
        return self.data.combatPlayerScore

    @property
    def cs(self):
        return self.minion_kills + self.monster_kills

    @property
    def deaths(self):
        """
        Returns:
            int: the number of deaths this participant had
        """
        return self.data.deaths

    @property
    def double_kills(self):
        """
        Returns:
            int: the number of double kills this participant had
        """
        return self.data.doubleKills

    @property
    def first_blood_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on first blood
        """
        return self.data.firstBloodAssist

    @property
    def first_blood(self):
        """
        Returns:
            bool: whether participant team got first blood
        """
        return self.data.firstBloodKill

    @property
    def first_inhibitor_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on the first inhibitor
        """
        return self.data.firstInhibitorAssist

    @property
    def first_inhibitor(self):
        """
        Returns:
            bool: flag indicating if this participant destroyed the first inhibitor
        """
        return self.data.firstInhibitorKill

    @property
    def first_turret_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on the first tower
        """
        return self.data.firstTowerAssist

    @property
    def first_turret(self):
        """
        Returns:
            bool: flag indicating if this team destroyed the first tower
        """
        return self.data.firstTowerKill

    @property
    def gold_earned(self):
        """
        Returns:
            int: the participant's total gold
        """
        return self.data.goldEarned

    @property
    def gold_spent(self):
        """
        Returns:
            int: the participant's spent gold
        """
        return self.data.goldSpent

    @property
    def inhibitor_kills(self):
        """
        Returns:
            int: the number of inhibitors this team killed
        """
        return self.data.inhibitorKills

    @property
    def item0(self):
        """
        Returns:
            Item: the participant's first item
        """
        return cassiopeia.riotapi.get_item(self.data.item0) if self.data.item0 else None

    @property
    def item1(self):
        """
        Returns:
            Item: the participant's second item
        """
        return cassiopeia.riotapi.get_item(self.data.item1) if self.data.item1 else None

    @property
    def item2(self):
        """
        Returns:
            Item: the participant's third item
        """
        return cassiopeia.riotapi.get_item(self.data.item2) if self.data.item2 else None

    @property
    def item3(self):
        """
        Returns:
            Item: the participant's fourth item
        """
        return cassiopeia.riotapi.get_item(self.data.item3) if self.data.item3 else None

    @property
    def item4(self):
        """
        Returns:
            Item: the participant's fifth item
        """
        return cassiopeia.riotapi.get_item(self.data.item4) if self.data.item4 else None

    @property
    def item5(self):
        return cassiopeia.riotapi.get_item(self.data.item5) if self.data.item5 else None

    @property
    def item6(self):
        """
        Returns:
            Item: the participant's seventh item (i.e. their ward)
        """
        return cassiopeia.riotapi.get_item(self.data.item6) if self.data.item6 else None

    @property
    def items(self):
        """
        Returns:
            list<Item>: the participant's items
        """
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def killing_sprees(self):
        """
        Returns:
            int: the number of killing sprees this participant had
        """
        return self.data.killingSprees

    @property
    def kills(self):
        """
        Returns:
            int: the total number of kills this participant had
        """
        return self.data.kills

    @property
    def largest_critical_strike(self):
        """
        Returns:
            int: the largest critical strike this participant had
        """
        return self.data.largestCriticalStrike

    @property
    def largest_killing_spree(self):
        """
        Returns:
            int: the larges killing spree this participant had
        """
        return self.data.largestKillingSpree

    @property
    def largest_multi_kill(self):
        """
        Returns:
            int: the largest multikill this participant had
        """
        return self.data.largestMultiKill

    @property
    def magic_damage_dealt(self):
        """
        Returns:
            int: the total magic damage this participant dealt
        """
        return self.data.magicDamageDealt

    @property
    def magic_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total magic damage this participant dealt to champions
        """
        return self.data.magicDamageDealtToChampions

    @property
    def magic_damage_taken(self):
        """
        Returns:
            int: the total magic damage this participant received
        """
        return self.data.magicDamageTaken

    @property
    def minion_kills(self):
        """
        Returns:
            int: the number of minions killed
        """
        return self.data.minionsKilled

    @property
    def monster_kills(self):
        """
        Returns:
            int: the number of neutral minions this participant killed
        """
        return self.data.neutralMinionsKilled

    @property
    def enemy_monster_kills(self):
        """
        Returns:
            int: the number of neutral jungle minions killed in the enemy team's jungle
        """
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def ally_monster_kills(self):
        """
        Returns:
            int: the number of neutral jungle minions killed in your team's jungle
        """
        return self.data.neutralMinionsKilledTeamJungle

    @property
    def nodes_captured(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant captured
        """
        return self.data.nodeCapture

    @property
    def node_capture_assists(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant assisted in capturing
        """
        return self.data.nodeCaptureAssist

    @property
    def node_neutralizations(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant neutralized
        """
        return self.data.nodeNeutralize

    @property
    def node_neutralization_assists(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant assisted in neutralizing
        """
        return self.data.nodeNeutralizeAssist

    @property
    def objective_score(self):
        """
        Returns:
            int: dominion only. the part of the participant's score that came from objective-related activities
        """
        return self.data.objectivePlayerScore

    @property
    def penta_kills(self):
        """
        Returns:
            int: the number of penta kills this participant had
        """
        return self.data.pentaKills

    @property
    def physical_damage_dealt(self):
        """
        Returns:
            int: the total physical damage this participant dealt
        """
        return self.data.physicalDamageDealt

    @property
    def physical_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total physical damage this participant dealt to champions
        """
        return self.data.physicalDamageDealtToChampions

    @property
    def physical_damage_taken(self):
        """
        Returns:
            int: the total physical damage this participant received
        """
        return self.data.physicalDamageTaken

    @property
    def quadra_kills(self):
        """
        Returns:
            int: the number of quadra kills this participant had
        """
        return self.data.quadraKills

    @property
    def sight_wards_bought(self):
        """
        Returns:
            int: the number of sight wards this participant bought
        """
        return self.data.sightWardsBoughtInGame

    @property
    def team_objectives(self):
        """
        Returns:
            int: if game was a dominion game, number of completed team objectives (i.e., quests)
        """
        return self.data.teamObjective

    @property
    def damage_dealt(self):
        """
        Returns:
            int: the total damage this participant dealt
        """
        return self.data.totalDamageDealt

    @property
    def damage_dealt_to_champions(self):
        """
        Returns:
            int: the total damage this participant dealt to champions
        """
        return self.data.totalDamageDealtToChampions

    @property
    def damage_taken(self):
        """
        Returns:
            int: the total damage this participant received
        """
        return self.data.totalDamageTaken

    @property
    def healing_done(self):
        """
        Returns:
            int: the amount of healing this participant did
        """
        return self.data.totalHeal

    @property
    def score(self):
        """
        Returns:
            int: dominion only. the score for this participant
        """
        return self.data.totalPlayerScore

    @property
    def score_rank(self):
        """
        Returns:
            int: if game was a dominion game, team rank of the player's total score (e.g., 1-5)
        """
        return self.data.totalScoreRank

    @property
    def crowd_control_dealt(self):
        """
        Returns:
            int: the total amount of crowd control this participant dealt (in seconds)
        """
        return self.data.totalTimeCrowdControlDealt

    @property
    def units_healed(self):
        """
        Returns:
            int: the number of units this participant healed
        """
        return self.data.totalUnitsHealed

    @property
    def turret_kills(self):
        """
        Returns:
            int: the number of turret kills this participant had
        """
        return self.data.towerKills

    @property
    def triple_kills(self):
        """
        Returns:
            int: the number of triple kills this participant had
        """
        return self.data.tripleKills

    @property
    def true_damage_dealt(self):
        """
        Returns:
            int: the total true damage this participant dealth
        """
        return self.data.trueDamageDealt

    @property
    def true_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total damage this participant dealt to champions
        """
        return self.data.trueDamageDealtToChampions

    @property
    def true_damage_taken(self):
        """
        Returns:
            int: the total true damage this participant received
        """
        return self.data.trueDamageTaken

    @property
    def unreal_kills(self):
        """
        Returns:
            int: the number of unreal kills this participant had
        """
        return self.data.unrealKills

    @property
    def vision_wards_bought(self):
        """
        Returns:
            int: the number of vision wards sprees this participant bought
        """
        return self.data.visionWardsBoughtInGame

    @property
    def ward_kills(self):
        """
        Returns:
            int: the number of wards this participant killed
        """
        return self.data.wardsKilled

    @property
    def wards_placed(self):
        """
        Returns:
            int: the number of wards this participant placed
        """
        return self.data.wardsPlaced

    @property
    def win(self):
        """
        Returns:
            bool: whether or not the participant won the game
        """
        return self.data.winner


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimeline(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantTimeline

    def __str__(self):
        return "Participant Timeline"

    @property
    def lane(self):
        """
        Returns:
            Lane: the lane this participant was in
        """
        lane = self.data.lane
        lane = "MIDDLE" if lane == "MID" else lane
        lane = "BOTTOM" if lane == "BOT" else lane
        return cassiopeia.type.core.common.Lane(lane) if lane else None

    @property
    def role(self):
        """
        Returns:
            Role: the role of this particiant
        """
        return cassiopeia.type.core.common.Role(self.data.role) if self.data.role else None



###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Match.dto_type = cassiopeia.type.dto.match.MatchDetail
    #Team.dto_type = cassiopeia.type.dto.match.Team
    #Timeline.dto_type = cassiopeia.type.dto.match.Timeline
    ParticipantStats.dto_type = cassiopeia.type.dto.match.ParticipantStats
    ParticipantTimeline.dto_type = cassiopeia.type.dto.match.ParticipantTimeline
    #Ban.dto_type = cassiopeia.type.dto.match.BannedChampion
    #Frame.dto_type = cassiopeia.type.dto.match.Frame
    #ParticipantTimelineData.dto_type = cassiopeia.type.dto.match.ParticipantTimelineData
    #Event.dto_type = cassiopeia.type.dto.match.Event
    #ParticipantFrame.dto_type = cassiopeia.type.dto.match.ParticipantFrame
    #Position.dto_type = cassiopeia.type.dto.match.Position
