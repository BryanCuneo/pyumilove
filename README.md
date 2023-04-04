# pyumilove
### A wrapper around [AyumiLove](https://ayumilove.net/), currently supporting portions of Raid: Shadow Legends and Awaken Chaos Era.
Intended for use with third-party tools such as Discord bots. Not associated with AyumiLove, I've just written this to make my life easier when trying to use game data in my other projects. Please support [their Patreon](https://www.patreon.com/ayumilove)!

## Raid: Shadow Legends
This library currently provides the following:
 * Champions - Name, faction, rarity, skills, role, affinity, rank, book count, and URL
 * Blessings - Name, description, awakening levels, and thumbnail image
 * Lists of all buffs and debuffs

## Awaken Chaos Era
This library currently provides the following:
 * Heroes - Name, faction, rarity, skills, type, element, and URL
 * Lists of all buffs and debuffs

## Example
<details>
<summary>Basic RSL champion search</summary>

```python
import asyncio

from pyumilove.raidshadowlegends import RSL


async def main():
    async with RSL() as client:
        while True:
            champ_name = input("Search for a champion ('q' to exit): ").lower()
            while champ_name == "":
                champ_name = input("Search for a champion ('q' to exit): ").lower()

            if champ_name.lower() == "q":
                print("\nExiting")
                break

            champ = await client.get_champion(champ_name)
            if champ:
                print(
                    "\n{0} - {1} - {2} - {3}".format(
                        champ.name, champ.affinity, champ.faction, champ.rarity
                    )
                )
                print("-" * 20, end="")
                [
                    print("\n{0}:\n{1}".format(skill["name"], skill["description"]))
                    for skill in champ.skills
                ]
                print("-" * 20, "\n")
            else:
                print("Unable to find champion named '{0}'.".format(champ_name))


if __name__ == "__main__":
    asyncio.run(main())
```
</details>

<details>

<summary>Results in:</summary>

```
$> python .\sample.py
Search for a champion ('q' to exit): ultimate deathknight

Ultimate Deathknight - Force - Undead Hordes - Legendary
--------------------
Heckler of Legends:
Attacks 1 enemy. Has a 30% chance of placing a [Provoke] debuff for 1 turn. The chance increases to 55% against Legendary Champions.

Rats Off To Ya (Cooldown: 4 turns):
Attacks all enemies. Has an 80% chance of placing a 50% [Decrease ATK] debuff for 2 turns. Also has an 80% chance of placing a [Fear] debuff for 1 turn on each Legendary Champion.

Get Comfy Everyone (Cooldown: 5 turns):
Places a [Shield] buff and a 15% [Continuous Heal] buff on all allies for 2 turns. The value of the [Shield] buff is proportional to this Champion’s DEF.

Too Awesome To Die (Passive):
Whenever an ally is attacked, has a 100% chance of completely blocking 1 hit, decreasing the damage to zero. This champion will receive that damage instead. The chance decrease to 50% if the attacker is a Boss. Does not work if the attack on the ally was an AoE attack. Whenever an enemy is healed, heals this champion by 20% of that heal.

Didn’t Need ‘Em (Passive):
Increase this Champion’s HP, DEF, and SPD by 10% for each dead ally.

Aura:
Increases Ally DEF in all Battles by 30%
--------------------

Search for a champion ('q' to exit): q

Exiting
$>
```
</details>
