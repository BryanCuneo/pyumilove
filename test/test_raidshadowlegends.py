import unittest

from bs4 import BeautifulSoup

from src.pyumilove.character import Character
from src.pyumilove.raidshadowlegends import Champion, Blessing, RSL
from src.pyumilove.skill import Skill


class TestRSL(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        champ_data = """<!DOCTYPE html><html><body><article><header><h1 class="entry-title">Siphi the Lost Bride | Raid Shadow Legends</h1></header><div><table><tbody><tr><td><h4>Overview</h4><p>NAME: Siphi the Lost Bride<br/>
FACTION: <a href="//ayumilove.net/raid-shadow-legends-list-of-champions-by-faction/#undeadhordes">Undead Hordes</a><br/>
RARITY: <a href="//ayumilove.net/raid-shadow-legends-list-of-champions-by-rarity/#legendary">Legendary</a><br/>
ROLE: <a href="//ayumilove.net/raid-shadow-legends-list-of-champions-by-role/#support">Support</a><br/>
AFFINITY: <a href="//ayumilove.net/raid-shadow-legends-list-of-champions-by-affinity/#void">Void</a><br/>
RANK: <a href="//ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/#legendary">S</a><br/>
USABILITY: Early-Mid-Late Game<br/>
TOMES: 10 (A1 A2 A3)</p><h4>Total Stats (6★)</h4> <p>Health Points (HP): 21,480<br/> Attack (ATK): 859<br/> Defense (DEF): 1,288<br/> Speed (SPD): 114<br/> Critical Rate (C.RATE): 15%<br/> Critical Damage (C.DMG): 50%<br/> Debuff Resistance (RESIST): 40<br/> Debuff Accuracy (ACC): 0</p><h4>Obtain from</h4> <p>Void Shard </td><td width="50%"> <h4>Grinding</h4> <p>★★★★✰ Campaign<br/> ★★★★★ Arena Defense<br/> ★★★★★ Arena Offense<br/> ★★★★★ Clan Boss<br/> ★★★★★ Faction Wars</p><h4>Dungeons</h4> <p>★★★★★ Minotaur<br/> ★★★★★ Spider<br/> ★★★★✰ Fire Knight<br/> ★★★★★ Dragon<br/> ★★★★★ Ice Golem</p><h4>Potion</h4> <p>★★★★★ Arcane Keep<br/> ★★★★★ Void Keep<br/> ★★★★★ Force Keep<br/> ★★★★★ Spirit Keep<br/> ★★★★★ Magic Keep</p><h4>Doom Tower</h4> <p>★★★★★ Floors<br/> ★★★★★ Magma Dragon<br/> ★★★★★ Nether Spider<br/> ★★★★★ Frost Spider<br/> ★★★★★ Scarab King<br/> ★✰✰✰✰ Celestial Griffin<br/> ★★★★★ Eternal Dragon<br/> ★★★★★ Dreadhorn<br/> ★★★✰✰ Dark Fae </td></tr></tbody></table>
<div id="AyumiloveArticleAd"></div>
<h2>Siphi the Lost Bride Skills</h2>
<p><strong>Curse of Longing [ATK]</strong><br/>
Attacks 1 enemy. Has an 80% chance of placing a [Sleep] debuff for 1 turn if the target’s Turn Meter is equal to or above 50%. This debuff cannot be resisted. Heals all allies by 5% of their MAX HP if the target’s Turn Meter is below 50%.<br/>
Level 2: Buff/Debuff Chance +5%<br/>
Level 3: Buff/Debuff Chance +5%<br/>
Level 4: Buff/Debuff Chance +5%<br/>
Level 5: Buff/Debuff Chance +5%<br/>
Damage Multiplier: 5 ATK</p>
<p><strong>Whirlwind Romance (Cooldown: 6 turns)</strong><br/>
Places a [Block Debuffs] buff on all allies for 2 turns, then fills the Turn Meters of all allies by 10% and places a 60% [Increase DEF] buff and a 30% [Increase SPD] buff on all allies for 2 turns.<br/>
Level 2: Cooldown -1<br/>
Level 3: Cooldown -1</p>
<p><strong>Love Beyond Death (Cooldown: 6 turns)</strong><br/>
Revives a single ally with 55% HP and a full Turn Meter. Places a 50% [Increase ATK] buff and a 30% [Increase C.RATE] buff on that ally for 2 turns.<br/>
Level 2: Cooldown -1<br/>
Level 3: Cooldown -1</p>
<p><strong>Eternal Bond [Passive]</strong><br/>
Heals each ally by 10% of their MAX HP at the start of their turn. Has a 40% chance of removing [Freeze] and [Fear] debuffs from each ally at the start of their turn. Removes all debuffs from <a href="https://ayumilove.net/raid-shadow-legends-rotos-the-lost-groom-skill-mastery-equip-guide/">Rotos the Lost Groom</a> at the start of their turn if they are on the same team.<br/>
Level 2: Buff/Debuff Chance +5%<br/>
Level 3: Buff/Debuff Chance +5%</p>
<p><strong>Aura</strong><br/>
Increases Ally RESIST in all Battles by 80.</p>
<p><input type="hidden" name="IL_IN_ARTICLE"></p></div></article></body></html>
"""

        blessings_data = """<!DOCTYPE html><html><body><div class="entry-content"><table><tbody><tr><td style="text-align:center" width="15%"><strong>Icon</strong></td><td style="text-align:center" width="90%"><strong>Rare Light Blessings Description</strong></td></tr>
<tr>
<td><img class="lazy loaded" decoding="async" src="//ayumilove.net/files/games/raid_shadow_legends/blessing/Indomitable_Spirit.jpg" data-src="//ayumilove.net/files/games/raid_shadow_legends/blessing/Indomitable_Spirit.jpg" alt="Indomitable Spirit - Raid Shadow Legends Rare Light Blessings" data-was-processed="true" width="188" height="247"></td>
<td>
<h4 id="indomitable-spirit">Indomitable Spirit</h4>
<ul>
<li>Has a chance of blocking any [Stun], [Sleep], and [Fear] debuffs whenever an enemy tries to place them on this Champion.</li>
</ul>
<h4>Awakening Level</h4>
<ol>
<li>5% chance of blocking debuffs</li>
<li>DEF +200 (+200 to Legendary Champions)</li>
<li>10% chance of blocking debuffs</li>
<li>HP +1000. ACC +30 (+20 to Legendary Champions)</li>
<li>15% chance of blocking debuffs</li>
<li>20% chance of blocking debuffs. SPD +5 (+5 to Legendary Champions)</li>
</ol>
<h4>Who should use this blessing?</h4>
<p>Indomitable Spirit blessing is utilized to block crowd control debuff from being applied to your champion by the enemies. The downside of this blessing is the success rate of blocking is low and it does not block all crowd control debuff. It’s recommended to go with a blessing that could provide increased Resist stat along with a wider range of crowd control debuff to be blocked, such as <a href="//ayumilove.net/raid-shadow-legends-champion-blessings-guide/#dark-resolve">Dark Resolve</a>. Having a high resistance stat will allow your champion to block all types of debuffs consistently and effectively making your battles more predictable.
</p></td></tr></tbody></table></div></body></html>
"""

        self.champ_soup = BeautifulSoup(champ_data, "lxml")
        self.siphi_url = "https://ayumilove.net/raid-shadow-legends-siphi-the-lost-bride-skill-mastery-equip-guide/"

        self.champs_exact_names = {
            "avirthealchemage": "https://ayumilove.net/raid-shadow-legends-avir-the-alchemage-skill-mastery-equip-guide/",
            "badelkazar": "https://ayumilove.net/raid-shadow-legends-bad-el-kazar-skill-mastery-equip-guide/",
            "bigun": "https://ayumilove.net/raid-shadow-legends-big-un-skill-mastery-equip-guide/",
        }

        self.champs_original_names = {
            "Avir the Alchemage": "https://ayumilove.net/raid-shadow-legends-avir-the-alchemage-skill-mastery-equip-guide/",
            "Bad-el-Kazar": "https://ayumilove.net/raid-shadow-legends-bad-el-kazar-skill-mastery-equip-guide/",
            "Big ‘Un": "https://ayumilove.net/raid-shadow-legends-big-un-skill-mastery-equip-guide/",
        }

        self.blessings_soup = BeautifulSoup(blessings_data, "lxml")
        self.blessing_upgrades = [
            "5% chance of blocking debuffs",
            "DEF +200 (+200 to Legendary Champions)",
            "10% chance of blocking debuffs",
            "HP +1000. ACC +30 (+20 to Legendary Champions)",
            "15% chance of blocking debuffs",
            "20% chance of blocking debuffs. SPD +5 (+5 to Legendary Champions)",
        ]

    def test_build_skills_from_soup(self):
        names = [
            "Curse of Longing [ATK]",
            "Whirlwind Romance (Cooldown: 6 turns)",
            "Love Beyond Death (Cooldown: 6 turns)",
            "Eternal Bond [Passive]",
            "Aura",
        ]
        descriptions = [
            "Attacks 1 enemy. Has an 80% chance of placing a [Sleep] debuff for 1 turn if the target’s Turn Meter is equal to or above 50%. This debuff cannot be resisted. Heals all allies by 5% of their MAX HP if the target’s Turn Meter is below 50%.",
            "Places a [Block Debuffs] buff on all allies for 2 turns, then fills the Turn Meters of all allies by 10% and places a 60% [Increase DEF] buff and a 30% [Increase SPD] buff on all allies for 2 turns.",
            "Revives a single ally with 55% HP and a full Turn Meter. Places a 50% [Increase ATK] buff and a 30% [Increase C.RATE] buff on that ally for 2 turns.",
            "Heals each ally by 10% of their MAX HP at the start of their turn. Has a 40% chance of removing [Freeze] and [Fear] debuffs from each ally at the start of their turn. Removes all debuffs from Rotos the Lost Groom at the start of their turn if they are on the same team.",
            "Increases Ally RESIST in all Battles by 80.",
        ]
        upgrades = [
            [
                "Level 2: Buff/Debuff Chance +5%",
                "Level 3: Buff/Debuff Chance +5%",
                "Level 4: Buff/Debuff Chance +5%",
                "Level 5: Buff/Debuff Chance +5%",
                "Damage Multiplier: 5 ATK",
            ],
            ["Level 2: Cooldown -1", "Level 3: Cooldown -1"],
            ["Level 2: Cooldown -1", "Level 3: Cooldown -1"],
            ["Level 2: Buff/Debuff Chance +5%", "Level 3: Buff/Debuff Chance +5%"],
            [],
        ]

        skills = RSL.build_skills_from_soup(self.champ_soup)

        self.assertEqual(len(skills), 5)

        for i in range(5):
            with self.subTest(skills[i].name):
                self.assertIsInstance(skills[i], Skill)

                self.assertEqual(skills[i].name, names[i])
                self.assertEqual(skills[i].description, descriptions[i])
                self.assertEqual(skills[i].upgrades, upgrades[i])

    def test_build_champion_from_soup(self):
        champion = RSL.build_champion_from_soup(self.champ_soup, self.siphi_url)

        self.assertIsInstance(champion, Character)
        self.assertIsInstance(champion, Champion)

        self.assertEqual(champion.name, "Siphi the Lost Bride")
        self.assertEqual(champion.faction, "Undead Hordes")
        self.assertEqual(champion.rarity, "Legendary")
        self.assertEqual(champion.role, "Support")
        self.assertEqual(champion.affinity, "Void")
        self.assertEqual(champion.rank, "S")
        self.assertEqual(champion.books, 10)
        self.assertEqual(champion.url, self.siphi_url)

    async def test_champion_list(self):
        async with RSL() as client:
            await client._set_character_list()

            self.assertIsInstance(client.character_list, dict)
            self.assertGreaterEqual(len(client.character_list), 677)

            for name in self.champs_exact_names:
                with self.subTest():
                    self.assertIn(name, client.character_list)

                with self.subTest():
                    self.assertEqual(
                        self.champs_exact_names[name], client.character_list[name]
                    )

            for name in self.champs_original_names:
                with self.subTest():
                    self.assertNotIn(name, client.character_list)

    async def test_champion_search(self):
        async with RSL() as client:

            all_champs = {**self.champs_exact_names, **self.champs_original_names}
            for name in all_champs:
                with self.subTest(name):
                    url, soup = await client.get_character_page(name)
                    self.assertIsInstance(soup, BeautifulSoup)
                    self.assertIsInstance(url, str)

                    champ = client.build_champion_from_soup(soup, all_champs[name])
                    self.assertIsInstance(champ, Character)
                    self.assertIsInstance(champ, Champion)

                    get_champ_result = await client.get_champion(name)
                    self.assertIsInstance(get_champ_result, Character)
                    self.assertIsInstance(get_champ_result, Champion)
                    self.assertEqual(champ, get_champ_result)

            no_soup = await client.get_character_page("aosnuteh")
            self.assertEqual(no_soup, (None, None))

            with self.assertRaises(AttributeError):
                client.build_champion_from_soup(no_soup, None)

    async def test_blessings(self):

        async with RSL() as client:

            blessings = client._build_blessings_from_soup(self.blessings_soup)
            blessing = blessings[0]
            self.assertIsInstance(blessings, list)
            self.assertIsInstance(blessing, Blessing)
            self.assertEqual(blessing.name, "Indomitable Spirit")
            self.assertEqual(
                blessing.description,
                "Has a chance of blocking any [Stun], [Sleep], and [Fear] debuffs whenever an enemy tries to place them on this Champion.",
            )
            self.assertEqual(len(blessing.awakening_levels), 6)
            self.assertEqual(blessing.awakening_levels, self.blessing_upgrades)
            self.assertEqual(
                blessing.image_url,
                "http://ayumilove.net/files/games/raid_shadow_legends/blessing/Indomitable_Spirit.jpg",
            )

            blessings = await client.blessings()
            self.assertEqual(len(blessings), 24)
