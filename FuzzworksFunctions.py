import json
import urllib.request

import ESIFunctions as Esi

HUB = {"Jita": "60003760",
       "Amarr": "60008494",
       "Dodixie": "60011866",
       "Rens": "60004588",
       "Hek": "60005686"}


def get_item_value(name):
    try:
        item_id = Esi.get_item_id(name)
        print(item_id)
        look_up_url = "https://market.fuzzwork.co.uk/aggregates/?" + \
                      "region=" + HUB["Jita"] + "&" \
                      "types=" + item_id
        search_res = urllib.request.urlopen(look_up_url)
        data = json.loads(search_res.read().decode())
        buy_price = 0
        buy_price = data[item_id]["buy"]["weightedAverage"]
        sell_price = 0
        sell_price = data[item_id]["sell"]["weightedAverage"]
        return "__**" + name + ":**__\n**Buy Price:** " + '{0:,.2f}'.format(float(buy_price)) +\
               "\n**Sell Price:** " + '{0:,.2f}'.format(float(sell_price)) + "\n"
    except KeyError:
        return "Item Not Found"