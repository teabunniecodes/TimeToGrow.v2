
from enum import Enum
from typing import Literal, TypedDict


# from .database import Database


class PlantType(Enum):
    BASIC = ("basic",)
    AUDREY = "audrey"


class PlantData(TypedDict):
    username: str
    plant_type: tuple[Literal["basic"]] | Literal["audrey"]
    state: int
    growth: int
    total: int
    wilted: bool
    dead: bool
    maxed: bool
    watering: bool
    blood_rain: bool
    glasses: bool
    speech: int
    top: int
