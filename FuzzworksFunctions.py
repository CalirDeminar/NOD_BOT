import json
import urllib.error
import urllib.request

import ESIFunctions as Esi

HUB = {"Jita": "60003760",
       "Amarr": "60008494"}

#{"Jita": "60003760",
#       "Amarr": "60008494",
#       "Dodixie": "60011866",
#       "Rens": "60004588",
#       "Hek": "60005686"}

fuel = {"Helium Fuel Block": "4247",
        "Oxygen Fuel Block": "4312",
        "Nitrogen Fuel Block": "4051",
        "Hydrogen Fuel Block": "4246"}


def get_item_value(name):
    """
    Retrieve the Buy and Sell Value of the specified item name from
    the precalculated daily market statistics for Jita
    Uses weighted average for buy and sell price

    :param name: Item name to be searched
    :return: Formatted string containing buy and sell prices for specified item
    """
    try:
        # get item ID from ESI
        item_id = Esi.get_item_id(name)
        print(item_id)
        # construct Fuzzworks market API URL
        look_up_url = "https://market.fuzzwork.co.uk/aggregates/?" + \
                      "region=" + HUB["Jita"] + "&" \
                      "types=" + item_id
        # request API
        search_res = urllib.request.urlopen(look_up_url)
        # unpack returned JSON
        data = json.loads(search_res.read().decode())
        buy_price = 0
        buy_price = data[item_id]["buy"]["weightedAverage"]
        sell_price = 0
        sell_price = data[item_id]["sell"]["weightedAverage"]
        #format output string
        return "__**" + name + ":**__\n**Buy Price:** " + '{0:,.2f}'.format(float(buy_price)) +\
               "\n**Sell Price:** " + '{0:,.2f}'.format(float(sell_price)) + "\n"
    except KeyError:
        return "Item Not Found"
    except urllib.error.HTTPError:
        return "Fuzzworks Not Responding"


def get_fuel_prices():
    """
    Get fuel block prices for all trade hubs in trade hub list
    Gets weighted average buy and sell values

    :return: Formatted string containing price of each fuel block at each trade hub in list
    """
    try:
        output = "**__Fuel Prices:__**\n"
        for hubName, hID in HUB.items():  # for each required tradeHub
            output += "**" + hubName + ":**\n"
            for fuelName, fID in fuel.items():  # for every fuel block type
                look_up_url = "https://market.fuzzwork.co.uk/aggregates/?" + \
                              "region=" + hID + "&" \
                              "types=" + fID
                # request API
                search_res = urllib.request.urlopen(look_up_url)
                # unpack returned JSON
                data = json.loads(search_res.read().decode())

                # format output string
                output += "     __" + fuelName + ":__\n"
                output += "         Buy: "
                output += str('{0:,.2f}'.format(float(data[fID]["buy"]["weightedAverage"])))

                output += "         Sell: "
                output += str('{0:,.2f}'.format(float(data[fID]["sell"]["weightedAverage"])))
                output += "\n"
        return output
    except urllib.error.HTTPError:
        return "Fuzzworks Not Responding"
