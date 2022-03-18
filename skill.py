from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str
    upgrades: list[str]
