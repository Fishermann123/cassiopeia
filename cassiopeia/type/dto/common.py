import json


class CassiopeiaDto(object):
    """
    A Python representation of an object returned by the Riot API
    """

    def __init__(self, dictionary):
        """
        Args:
            dictionary (dict): the JSON data returned from the Riot API as a dict
        """
        for key, value in dictionary.items():
            setattr(self, key, value)

    def to_json(self, **kwargs):
        """Gets a JSON representation of the object

        Returns:
            str: a JSON representation of the object
        """
        dictionary = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        default = kwargs.pop("default", lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith("_")})
        return json.dumps(dictionary, default=default, **kwargs)

    @property
    def champion_ids(self):
        """
        Returns:
            set: the champion IDs that are contained within this object (including nested ones)
        """
        return set()

    def __str__(self):
        return self.to_json(indent=4, sort_keys=True)

    def __repr__(self):
        return "{class_}({dict_})".format(class_=self.__class__.__name__, dict_=self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ if other else False

    def __ne__(self, other):
        return self.__dict__ != other.__dict__ if other else True

    def __hash__(self):
        return hash(id(self))
