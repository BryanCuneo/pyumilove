import asyncio
import aiohttp
from bs4 import BeautifulSoup

from character import Character
from skill import Skill


class AyumiLoveClient:
    _base_url = "https://ayumilove.net"
    _headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
    }

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
            name=details[0].split(": ", 1)[-1],
            faction=details[1].split(": ", 1)[-1],
            rarity=details[2].split(": ", 1)[-1],
            skills=AyumiLoveClient.build_skills_from_soup(soup),
            url=url,
        )

    def __init__(self, game):
        self.client = aiohttp.ClientSession(headers=AyumiLoveClient._headers)
        self.game = game.lower()

    async def _close(self):
        return await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close()
        return None

    async def _get_soup(self, url):
        response = await self.client.get(url)
        soup = BeautifulSoup(await response.text(), "lxml")
        return soup

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
