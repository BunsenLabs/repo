""" A pointer commands APT to fetch something from an origin. A pointer
is represented on the system by a valid, active entry in APT's
sources.list configuration system."""

from dataclasses import dataclass
from typing import List
from enum import Enum

from pydantic import BaseModel, AnyHttpUrl

class Type(str, Enum):
    BINARY = "deb"
    SOURCE = "deb-src"

class Distribution(BaseModel):
    name: str

class Component(BaseModel):
    name: str

class Origin(BaseModel):
    url: AnyHttpUrl

class Pointer(BaseModel):
    type: Type
    origin: Origin
    distribution: Distribution
    components: List[Component]
