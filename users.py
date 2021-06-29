from typing import Optional, Union
import discord
import enum

class BodyPart(enum.Enum):
    MOUTH = "mouth"
    ARMS = "arms"

class Gag(enum.Enum):
    BALLGAG = "large ballgag"

class ArmRestraint(enum.Enum):
    CUFFS = "handcuffs"

RESTRAINT = Union[Gag, ArmRestraint]

class User:
    def __init__(self, username):
        self.username = username
        self.restraints = RestraintSet()

    @property
    def is_gagged(self):
        return self.restraints.mouth is not None

    @property
    def can_interact(self):
        return self.restraints.arms is None

    def bind(self, restraint: RESTRAINT):
        if isinstance(restraint, Gag):
            self.restraints.mouth = restraint
        elif isinstance(restraint, ArmRestraint):
            self.restraints.arms = restraint

    def unbind(self, bodypart: BodyPart):
        setattr(self.restraints, bodypart.value, None)




class RestraintSet:
    def __init__(self):
        self.mouth: Optional[Gag] = None
        self.arms: Optional[ArmRestraint] = None


USERS = {}

def get_user(member: discord.Member):
    username = str(member)

    saved_user = USERS.get(username)

    # Create a new user if we need one
    if saved_user is None:
        saved_user = User(username)
        USERS[username] = saved_user

    return saved_user
