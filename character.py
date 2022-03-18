from dataclasses import dataclass

from skill import Skill


@dataclass
class Character:
    """Base class for an game character."""

    name: str
    faction: str
    rarity: str
    skills: list[Skill]
    url: str
