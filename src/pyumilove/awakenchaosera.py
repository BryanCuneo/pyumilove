import asyncio
from dataclasses import asdict, dataclass

from .character import Character
from .client import AyumiLoveClient


@dataclass
class Hero(Character):
    element: str
    heroType: str

    @classmethod
    def from_parent(self, parent_instance, element, heroType):
        new_attributes = {"element": element, "heroType": heroType}

        return self(**asdict(parent_instance), **new_attributes)


class ACE(AyumiLoveClient):
    @staticmethod
    def build_character_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        element = details[3].split(": ", 1)[-1]
        heroType = details[4].split(": ", 1)[-1]

        return Hero.from_parent(
            super(ACE, ACE).build_character_from_soup(soup, url), element, heroType
        )

    def __init__(self):
        super().__init__("awaken chaos era")

    async def hero_search(self, hero_name):
        hero_url = await self.search(hero_name)
        hero_soup = await self._get_soup(hero_url)

        return ACE.build_character_from_soup(hero_soup, hero_url)
