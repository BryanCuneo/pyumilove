import asyncio
from dataclasses import asdict, dataclass

from .character import Character
from .client import AyumiLoveClient


@dataclass
class Champion(Character):
    role: str
    affinity: str
    rank: chr
    books: int

    @classmethod
    def from_parent(cls, parent_instance, role, affinity, rank, books):
        new_attributes = {
            "role": role,
            "affinity": affinity,
            "rank": rank,
            "books": books,
        }

        return cls(**asdict(parent_instance), **new_attributes)


@dataclass
class Blessing:
    name: str
    description: str
    awakening_levels: list[str]
    image_url: str

    @classmethod
    def from_soup_table_row(cls, table_row):
        name = table_row.h4.text
        description = table_row.ul.li.text
        awakening_levels = [item.text for item in table_row.ol.find_all("li")]
        url = "http:" + table_row.img["src"]

        new_attributes = {
            "name": name,
            "description": description,
            "awakening_levels": awakening_levels,
            "image_url": url,
        }

        return cls(**new_attributes)


class RSL(AyumiLoveClient):
    _rsl_url = AyumiLoveClient._base_url + "/raid-shadow-legends-guide"
    _blessings_url = (
        AyumiLoveClient._base_url + "/raid-shadow-legends-champion-blessings-guide"
    )

    @staticmethod
    def build_champion_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        role = details[3].partition(": ")[2]
        affinity = details[4].partition(": ")[2]
        rank = details[5].partition(": ")[2]
        books = details[7].partition(": ")[2]
        books = int(books.partition(" ")[0])

        return Champion.from_parent(
            super(RSL, RSL).build_character_from_soup(soup, url),
            role,
            affinity,
            rank,
            books,
        )

    @staticmethod
    def _build_blessings_from_soup(blessings_soup):
        # First row in the table is a header. Ignore it
        rows = [row for row in blessings_soup.find_all("tr") if row.h4]
        blessings = [Blessing.from_soup_table_row(row) for row in rows]

        return blessings

    def __init__(self):
        super().__init__(AyumiLoveClient.RAID_SHADOW_LEGENDS)

    async def _get_blessings(self):
        soup = await self._get_soup(self._blessings_url)
        return self._build_blessings_from_soup(soup)

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

    async def blessings(self):
        return await self._get_blessings()
