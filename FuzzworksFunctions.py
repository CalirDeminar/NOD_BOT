import json
import urllib.request

import ESIFunctions as Esi


def get_item_value(name):
    item_id = Esi.get_item_id(name)
    look_up_url = "https://market.fuzzwork.co.uk/aggregates/?region=10000002&types=" + item_id
    search_res = urllib.request.urlopen(look_up_url)
    data = json.loads(search_res.read().decode())
    buy_price = 0
    sell_price = 0
    buy_price = data[item_id]["buy"]["weightedAverage"]
    sell_price = data[item_id]["sell"]["weightedAverage"]
    return "__**" + name + ":**__\n**Buy Price:** " + '{0:,.2f}'.format(float(buy_price)) +\
           "\n**Sell Price:** " + '{0:,.2f}'.format(float(sell_price)) + "\n"
