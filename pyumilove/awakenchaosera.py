import asyncio
from dataclasses import asdict, dataclass

from .character import Character
from .client import AyumiLoveClient


@dataclass
class Hero(Character):
    element: str
    heroType: str

    @classmethod
    def from_parent(cls, parent_instance, element, heroType):
        new_attributes = {"element": element, "heroType": heroType}

        return cls(**asdict(parent_instance), **new_attributes)


class ACE(AyumiLoveClient):
    _ace_url = AyumiLoveClient._base_url + "/awaken-chaos-era-guide"

    @staticmethod
    def build_hero_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        element = details[3].partition(": ")[2]
        heroType = details[4].partition(": ")[2]

        return Hero.from_parent(
            super(ACE, ACE).build_character_from_soup(soup, url), element, heroType
        )

    def __init__(self):
        super().__init__(AyumiLoveClient.AWAKEN_CHAOS_ERA)

    async def get_hero(self, hero_name):
        url, soup = await self.get_character_page(hero_name)
        try:
            hero = ACE.build_hero_from_soup(soup, url)
        except AttributeError:
            hero = None

        return hero

    async def buffs(self):
        return await self._get_table_links(ACE._ace_url, "Buff (Positive Effect)")

    async def debuffs(self):
        return await self._get_table_links(ACE._ace_url, "Debuff (Negative Effect)")
