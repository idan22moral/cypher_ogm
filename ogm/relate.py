from ogm.base import (
    BaseNode,
    RelOrRelType,
    RelationshipType,
    try_instantiate,
)
from ogm.relationship import RelationshipDirection


class Relate:
    def __init__(
        self,
        relationship: RelOrRelType,
        related_node_type: type[BaseNode],
        direction: RelationshipDirection,
    ):
        self._relationship = try_instantiate(relationship)
        self._type = RelationshipType.ONE_TO_ONE
        self._target = related_node_type
        self._direction = direction

    def __get__(self, obj: BaseNode, objtype=None):
        self._target = try_instantiate(self._target)
        self._relationship.parent = try_instantiate(obj)
        self._target.relationship = self._relationship
        self._target.relationship_type = self._type
        return self._target

    def __set_name__(self, owner, name: str):
        if not issubclass(owner, BaseNode):
            raise TypeError("relationships can be assigned to nodes only")
