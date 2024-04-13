import datetime
from typing import ClassVar, Optional

from ogm.base import BaseNode, BaseRelationship
from ogm.relate import Relate
from ogm.relationship import RelationshipDirection


class WorksIn(BaseRelationship):
    start_date: Optional[datetime.date] = None


class LivesIn(BaseRelationship):
    start_date: Optional[datetime.date] = None


class Workplace(BaseNode):
    name: Optional[str] = None
    worker: ClassVar = Relate(WorksIn, BaseNode, RelationshipDirection.INCOMING)


class City(BaseNode):
    name: Optional[str] = None

    citizen: ClassVar = Relate(LivesIn, BaseNode, RelationshipDirection.INCOMING)


class Person(BaseNode):
    name: Optional[str] = None

    workplace: ClassVar = Relate(WorksIn, Workplace, RelationshipDirection.OUTGOING)
    hometown: ClassVar = Relate(LivesIn, City, RelationshipDirection.OUTGOING)


Workplace.worker = Relate(WorksIn, Person, RelationshipDirection.INCOMING)
City.citizen = Relate(LivesIn, Person, RelationshipDirection.INCOMING)


john = Person(name="bob")
my_workplace = Workplace(name="MyWorkplace")

print(john.workplace.find_one())
print(my_workplace.worker.find_one())
print(City().citizen(Person(name="alice")).find_one())
