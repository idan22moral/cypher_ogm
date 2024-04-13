from typing import Self

from pydantic import Field, PrivateAttr

from ogm.entity import BaseEntity
from ogm.relationship import RelationshipType

type RelOrRelType = "BaseRelationship | type[BaseRelationship]"
type NodeOrNodeType = "BaseNode | type[BaseNode]"


def try_instantiate(entity):
    if entity is None:
        return entity
    if isinstance(entity, BaseEntity):
        return entity
    return entity()


class BaseNode(BaseEntity):
    def __str__(self) -> str:
        return "({node})".format(node=super().__str__())

    _relationship: RelOrRelType | None = PrivateAttr(default=None)
    _relationship_type: RelationshipType | None = PrivateAttr(default=None)

    @property
    def relationship(self):
        return self._relationship

    @relationship.setter
    def relationship(self, relationship: RelOrRelType | None):
        self._relationship = relationship

    @property
    def relationship_type(self):
        return self._relationship_type

    @relationship_type.setter
    def relationship_type(self, relationship_type: RelationshipType | None):
        self._relationship_type = relationship_type

    def __call__(self, node: NodeOrNodeType | None = None):
        node = try_instantiate(node) or self
        node.relationship = self.relationship
        return node

    def find_one(self: Self):
        if self.relationship:
            return "{relationship}-{self}".format(
                relationship=self.relationship,
                self=self,
            )
        return "{self}".format(self=self)

    @classmethod
    def find_one_cls(cls):
        if cls.relationship:
            return "{relationship}-{cls}".format(
                relationship=cls.relationship,
                cls=cls,
            )
        return "{cls}".format(cls=cls)


class BaseRelationship(BaseEntity):
    parent: NodeOrNodeType | None = Field(init=False, default=None, exclude=True)

    def __call__(self, relationship: RelOrRelType | None = None):
        return relationship or self

    def __str__(self) -> str:
        return "{parent}-[{relationship}]".format(
            parent=self.parent,
            relationship=super().__str__(),
        )
