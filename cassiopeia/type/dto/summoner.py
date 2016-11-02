import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class Summoner(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all mastery IDs contained in this object
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        #self.profileIconId = dictionary.get("profileIconId", 0)
        #self.revisionDate = dictionary.get("revisionDate", 0)
        #self.summonerLevel = dictionary.get("summonerLevel", 0)


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_summoner():
    global Summoner

    @cassiopeia.type.core.common.inheritdocs
    class Summoner(Summoner, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Summoner"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        #profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        #revisionDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        #summonerLevel = sqlalchemy.Column(sqlalchemy.Integer)


def _sa_bind_all():
    #_sa_bind_rune_page()
    #_sa_bind_rune_slot()
    #_sa_bind_mastery_page()
    #_sa_bind_mastery()
    _sa_bind_summoner()
