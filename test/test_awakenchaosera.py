import unittest
from bs4 import BeautifulSoup

from src.pyumilove.character import Character
from src.pyumilove.awakenchaosera import Hero, ACE
from src.pyumilove.skill import Skill


class TestACE(unittest.TestCase):
    def setUp(self):
        data = """<!DOCTYPE html><html><body><article><header><h1 class="entry-title">Celestial Kane | Awaken Chaos Era</h1></header><div><table><tbody><tr><td><h4>Overview</h4><p>NAME: Celestial Kane<br/>
        FACTION: <a href="//ayumilove.net/awaken-chaos-era-hero-by-faction/#sylvan-woodlands">Sylvan Woodlands</a><br/>
        RARITY: <a href="//ayumilove.net/awaken-chaos-era-hero-by-rarity/#epic">Epic</a><br/>
        ELEMENT: <a href="//ayumilove.net/awaken-chaos-era-hero-by-element/#light">Light</a><br/>
        TYPE: <a href="//ayumilove.net/awaken-chaos-era-hero-by-type/#defense">Defense</a></td><td><h4>Grinding</h4><p>★★★★✰ Adventure<br/>★★★★✰ Guild Boss<br/>★★★★★ Arena Offense<br/>★★★★★ Arena Defense</p><h4>No Man&#8217;s Land</h4><p>★★★★✰ Bane Wraith<br/>★★★★✰ Flame Lizard<br/>★★★★✰ Wrathful Flood<br/>★★★★✰ Lord of Holy Light<br/>★★★★★ Shadow Captive</p><h4>Arcane Dominator</h4><p>★★★★✰ Roaring Tulpa<br/>★★★★★ Ash Magisteria<br/>★★★★★ Queen of Tides<br/>★★★★★ Witch of Wind<br/>★★★★✰ Gemini Dragon</td></tr></tbody></table><div id="AyumiloveArticleAd"></div>
        <h2>Celestial Kane Skills</h2>
        <p><strong>Natural Healing (Trait)</strong><br/>
        When this character is attacked, remove 1 negative effect from each of 2 team members. Can only be triggered once per turn.<br/>
        [Ascension] Removes 1 negative effect from all team members when this character is attacked. Can only be triggered once per turn.</p>
        <p><strong>Bear Claw (Basic)</strong><br/>
        Deals 2 to 6 strikes of 30% damage to an enemy. Each strike heals this character for 4% of Max Health.<br/>
        Level 2: Damage +5%.<br/>
        Level 3: Damage +5%.</p>
        <p><strong>Collision (Special, Cooldown: 3 turns)</strong><br/>
        Deals 100% damage to an enemy and applies Taunt for 1 turn.<br/>
        Level 2: Damage +10%.<br/>
        Level 3: Ability cooldown is reduced by 1 turn.<br/>
        Level 4: Damage +10%.<br/>
        Taunt : Immune to control effects. Automatically uses basic ability to attack the caster. [Control Effect]</p>
        <p><strong>High Ground (Ultimate, Cooldown: 4 turns)</strong><br/>
        Deals 100% damage to all enemies and grants <a href="//ayumilove.net/ace-skill-invincible/">Invincible</a> to all team members for 1 turn.<br/>
        Level 2: Damage +10%.<br/>
        Level 3: Ability cooldown is reduced by 1 turn.<br/>
        Level 4: Damage +10%.<br/>
        Level 5: Ability cooldown is reduced by 1 turn.</p>
        <p><input type="hidden" name="IL_IN_ARTICLE"></p></div></article></body></html>
        """
        self.soup = BeautifulSoup(data, "lxml")
        self.url = "https://ayumilove.net/ace-hero-guide-celestial-kane/"

    def test_build_skills_from_soup(self):
        names = [
            "Natural Healing (Trait)",
            "Bear Claw (Basic)",
            "Collision (Special, Cooldown: 3 turns)",
            "High Ground (Ultimate, Cooldown: 4 turns)",
        ]
        descriptions = [
            "When this character is attacked, remove 1 negative effect from each of 2 team members. Can only be triggered once per turn.",
            "Deals 2 to 6 strikes of 30% damage to an enemy. Each strike heals this character for 4% of Max Health.",
            "Deals 100% damage to an enemy and applies Taunt for 1 turn.",
            "Deals 100% damage to all enemies and grants Invincible to all team members for 1 turn.",
        ]
        upgrades = [
            [
                "[Ascension] Removes 1 negative effect from all team members when this character is attacked. Can only be triggered once per turn."
            ],
            ["Level 2: Damage +5%.", "Level 3: Damage +5%."],
            [
                "Level 2: Damage +10%.",
                "Level 3: Ability cooldown is reduced by 1 turn.",
                "Level 4: Damage +10%.",
                "Taunt : Immune to control effects. Automatically uses basic ability to attack the caster. [Control Effect]",
            ],
            [
                "Level 2: Damage +10%.",
                "Level 3: Ability cooldown is reduced by 1 turn.",
                "Level 4: Damage +10%.",
                "Level 5: Ability cooldown is reduced by 1 turn.",
            ],
        ]

        skills = ACE.build_skills_from_soup(self.soup)

        self.assertEqual(len(skills), 4)

        for i in range(4):
            with self.subTest(skills[i].name):
                self.assertIsInstance(skills[i], Skill)

                self.assertEqual(skills[i].name, names[i])
                self.assertEqual(skills[i].description, descriptions[i])
                self.assertEqual(skills[i].upgrades, upgrades[i])

    def test_build_champion_from_soup(self):
        hero = ACE.build_character_from_soup(self.soup, self.url)

        self.assertIsInstance(hero, Character)
        self.assertIsInstance(hero, Hero)

        self.assertEqual(hero.name, "Celestial Kane")
        self.assertEqual(hero.faction, "Sylvan Woodlands")
        self.assertEqual(hero.rarity, "Epic")
        self.assertEqual(hero.element, "Light")
        self.assertEqual(hero.heroType, "Defense")
        self.assertEqual(hero.url, self.url)
