from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class EntityType(str, Enum):
    DESTINATION = "DESTINATION"
    PARK = "PARK"
    ATTRACTION = "ATTRACTION"
    SHOW = "SHOW"
    RESTAURANT = "RESTAURANT"
    HOTEL = "HOTEL"


class Location(BaseModel):
    latitude: float
    longitude: float


class Tag(BaseModel):
    tag: str
    tagName: str
    id: Optional[str] = None
    value: Any


class Entity(BaseModel):
    id: str
    name: str
    entityType: EntityType
    parentId: Optional[str] = None
    destinationId: Optional[str] = None
    parkId: Optional[str] = None
    timezone: Optional[str] = None
    location: Optional[Location] = None
    tags: list[Tag] = []


class ChildrenResponse(BaseModel):
    children: list[Entity]