import asyncio
from dataclasses import asdict, dataclass

from .character import Character
from .client import AyumiLoveClient


@dataclass
class Champion(Character):
    role: str
    affinity: str
    books: int

    @classmethod
    def from_parent(cls, parent_instance, role, affinity, books):
        new_attributes = {"role": role, "affinity": affinity, "books": books}

        return cls(**asdict(parent_instance), **new_attributes)


class RSL(AyumiLoveClient):
    _rsl_url = AyumiLoveClient._base_url + "/raid-shadow-legends-guide"

    @staticmethod
    def build_champion_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        role = details[3].partition(": ")[2]
        affinity = details[4].partition(": ")[2]
        books = details[6].partition(": ")[2]
        books = int(books.partition(" ")[0])

        return Champion.from_parent(
            super(RSL, RSL).build_character_from_soup(soup, url), role, affinity, books
        )

    def __init__(self):
        super().__init__(AyumiLoveClient.RAID_SHADOW_LEGENDS)

    async def get_champion(self, champ_name):
        url, soup = await self.get_character_page(champ_name)
        try:
            champ = RSL.build_champion_from_soup(soup, url)
        except AttributeError:
            champ = None

        return champ

    async def buffs(self):
        return await self._get_table_links(RSL._rsl_url, "Buff")

    async def debuffs(self):
        return await self._get_table_links(RSL._rsl_url, "Debuff")
