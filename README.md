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
