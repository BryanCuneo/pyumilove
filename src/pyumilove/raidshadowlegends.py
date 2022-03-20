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
    def build_character_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        role = details[3].split(": ", 1)[-1]
        affinity = details[4].split(": ", 1)[-1]
        books = details[6].split(": ", 1)[-1]
        books = int(books.split(" ", 1)[0])

        return Champion.from_parent(
            super(RSL, RSL).build_character_from_soup(soup, url), role, affinity, books
        )

    def __init__(self):
        super().__init__("raid shadow legends")

    async def champ_search(self, champ_name):
        champ_url = await self.search(champ_name)
        champ_soup = await self._get_soup(champ_url)

        return RSL.build_character_from_soup(champ_soup, champ_url)

    async def buffs(self):
        return await self._get_table_links(RSL._rsl_url, "Buff")

    async def debuffs(self):
        return await self._get_table_links(RSL._rsl_url, "Debuff")
