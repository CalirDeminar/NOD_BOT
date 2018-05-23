import json
import urllib.request

url = "https://esi.evetech.net/latest/characters/96167789/notifications/?datasource=tranquility"

# store zkill stat result
kb_sum = urllib.request.urlopen(url)

# convert zkill output
data = json.loads(kb_sum.read().decode())
print(data)