import requests, sys

BASE_URL = "https://ddragon.leagueoflegends.com/cdn/15.16.1/data/fr_FR/champion"

for arg in sys.argv[1:]:
    champ = arg[0].capitalize() + arg[1:].lower()
    try:
        data = requests.get(f"{BASE_URL}/{champ}.json").json()["data"][champ]["spells"]
        cooldown = [
            f'Q: {" / ".join(f'\33[1;34m{str(x)}\33[0m' for x in data[0]["cooldown"])}',
            f'W: {" / ".join(f'\33[1;34m{str(x)}\33[0m' for x in data[1]["cooldown"])}',
            f'E: {" / ".join(f'\33[1;34m{str(x)}\33[0m' for x in data[2]["cooldown"])}',
            f'R: {" / ".join(f'\33[1;34m{str(x)}\33[0m' for x in data[3]["cooldown"])}'
        ]
        print(f"\33[1;33m////////// League helper : cooldowns for {champ}\33[0m")
        for v in cooldown: print(v)
    except: print(f"\33[1;31mFailed to find cooldowns for {champ}\33[0m")
