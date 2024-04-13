from enum import Enum, auto


class RelationshipType(Enum):
    ONE_TO_ONE = auto()
    ONE_TO_MANY = auto()


class RelationshipDirection(Enum):
    INCOMING = auto()
    OUTGOING = auto()
