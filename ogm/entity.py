import random
import string
from typing import ClassVar

from pydantic import BaseModel, Field


def _unique_id():
    return "".join(random.choices(string.ascii_uppercase, k=5))


class BaseEntity(BaseModel):
    __subclasses: ClassVar[set[str]] = set()

    id: str = Field(exclude=True, default_factory=_unique_id, init=False)

    def __init_subclass__(cls, **kwargs) -> None:
        # prevent defining of multiple entities with the same name
        if str(cls.__name__) in cls.__subclasses:
            raise KeyError("entity type name already taken")
        cls.__subclasses.add(cls.__name__)
        super().__init_subclass__(**kwargs)

    @property
    def type_name(self):
        return self.__class__.__name__

    @property
    def variable_name(self):
        return "{type}_{id}".format(type=self.type_name.lower(), id=self.id)

    def __str__(self) -> str:
        formatted_properties = ", ".join(
            [
                f"`{k}`: {repr(v)}"
                for k, v in self.model_dump(mode="json", exclude_unset=True).items()
            ]
        )
        if formatted_properties:
            return "({variable_name}:{type} {{ {properties} }})".format(
                variable_name=self.variable_name,
                type=self.type_name,
                properties=formatted_properties,
            )

        return "({variable_name}:{type})".format(
            variable_name=self.variable_name,
            type=self.type_name,
        )
