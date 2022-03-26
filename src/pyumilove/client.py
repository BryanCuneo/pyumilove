import asyncio

import aiohttp
from bs4 import BeautifulSoup

from .character import Character
from .skill import Skill


class AyumiLoveClient:
    AWAKEN_CHAOS_ERA = "awaken chaos era"
    RAID_SHADOW_LEGENDS = "raid shadow legends"

    _base_url = "https://ayumilove.net"
    _headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
    }

    character_list = None

    @staticmethod
    def build_skills_from_soup(soup):
        skills = []

        character_name = soup.find("h1", {"class": "entry-title"}).text.split(" | ", 1)[
            0
        ]
        skill_element = soup.find(
            "h2", text=character_name + " Skills"
        ).next_sibling.next_sibling

        while skill_element.text != "":
            skill_details = [s.strip() for s in skill_element.text.split("\n")]
            skills.append(
                Skill(
                    name=skill_details[0],
                    description=skill_details[1],
                    upgrades=skill_details[2:],
                )
            )

            skill_element = skill_element.next_sibling.next_sibling

        return skills

    @staticmethod
    def build_character_from_soup(soup, url):
        details = [t.strip() for t in soup.tr.p.text.split("\n")]

        return Character(
            name=details[0].partition(": ")[2],
            faction=details[1].partition(": ")[2],
            rarity=details[2].partition(": ")[2],
            skills=AyumiLoveClient.build_skills_from_soup(soup),
            url=url,
        )

    @staticmethod
    def parse_character_name(name):
        """Parse a stripped-down name out of a name-string.

        "Avir the Alchemage (DW-RSM)" -> "avirthealchemage"
        "Marian Shadowblood (LA-EOD)" -> "marianshadowblood"
        "Ma’Shalled (UH-LAS)" -> "mashalled"
        """
        return "".join(c for c in name.partition("(")[0].lower() if c.isalpha())

    def __init__(self, game):
        self.game = game.lower()
        if (
            self.game != AyumiLoveClient.AWAKEN_CHAOS_ERA
            and self.game != AyumiLoveClient.RAID_SHADOW_LEGENDS
        ):
            error = ValueError()
            error.strerror = "'{0}' is not a valid game."
            raise error

        self.client = aiohttp.ClientSession(headers=AyumiLoveClient._headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return None

    async def _get_soup(self, url):
        response = await self.client.get(url)
        soup = BeautifulSoup(await response.text(), "lxml")
        return soup

    async def _get_table_links(self, url, section):
        soup = await self._get_soup(url)
        links = soup.find("h4", text=section).next_sibling.next_sibling.findChildren(
            "a"
        )

        return {elem.text: "https:" + elem["href"] for elem in links}

    async def _set_character_list(self):
        if self.game == AyumiLoveClient.AWAKEN_CHAOS_ERA:
            url = "https://ayumilove.net/ace-hero-by-element/"
        else:  # self.game == AyumiLoveClient.RAID_SHADOW_LEGENDS:
            url = "https://ayumilove.net/raid-shadow-legends-list-of-champions-by-affinity/"

        soup = await self._get_soup(url)

        AyumiLoveClient.character_list = {
            AyumiLoveClient.parse_character_name(elem.text): "https:" + elem["href"]
            for elem in soup.article.find_all("a")
        }

    async def close(self):
        return await self.client.close()

    async def get_character_page(self, character_name):
        if not AyumiLoveClient.character_list:
            await self._set_character_list()

        try:
            clean_name = AyumiLoveClient.parse_character_name(character_name)
            url = AyumiLoveClient.character_list[clean_name]
            soup = await self._get_soup(url)
        except KeyError:
            try:
                url = await self.search(character_name)
                soup = await self._get_soup(url)
            except TypeError:
                url = None
                soup = None

        return (url, soup)

    async def search(self, query):
        url = "{0}/?s={1}".format(AyumiLoveClient._base_url, query)
        soup = await self._get_soup(url)
        result = None
        try:
            element = soup.ol.li
        except AttributeError:
            element = None

        while element:
            if self.game in element.a.text.lower():
                result = element.a["href"]
                element = None
            else:
                element = element.next_sibling.next_sibling

        return result
