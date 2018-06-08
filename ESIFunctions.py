import json
import urllib.error
import urllib.request


def get_corp_id(name):
    """
    Searches the EvE database for a corp ID matching the full corp name, or ticker specified

    :param name: The full corp name, or corp ticker, to be searched for
    :return: The corp_id for the specified corp
    """
    try:
        print("Getting Corp ID")

        fixed_name = (name.replace(" ", "%20")).replace("-", "%2D")
        print(fixed_name)
        # lookup corp ID from ESI
        look_up_url = "https://esi.evetech.net/latest/" \
                      "search/" \
                      "?categories=corporation&" \
                      "datasource=tranquility&" + \
                      "language=en-us&" \
                      "search=" + fixed_name + \
                      "&strict=true"
        # store lookup result
        search_res = urllib.request.urlopen(look_up_url)
        # strip square brackets and store as string
        return str(json.loads(search_res.read().decode())["corporation"]).strip("[").strip("]")
    except urllib.error.HTTPError:
        return "ESI Not Responding"
    except urllib.error.URLError:
        return "Corp Not Found"


def get_char_id(name):
    """
    Searches the EvE database for a character ID matching the full character name specified

    :param name: The full character name to be searched for
    :return: The character_id for the specified character
    """
    try:
        print("Getting Char ID")
        fixed_name = name.replace(" ", "%20")
        # lookup corp ID from ESI
        look_up_url = "https://esi.evetech.net/latest/" \
                      "search/" \
                      "?categories=character&" \
                      "datasource=tranquility&" \
                      "language=en-us&search=" + fixed_name + \
                      "&strict=true"
        # store lookup result
        search_res = urllib.request.urlopen(look_up_url)
        # strip square brackets and store as string
        return str(json.loads(search_res.read().decode())["character"]).strip("[").strip("]")
    except urllib.error.HTTPError:
        return "ESI Not Responding"
    except urllib.error.URLError:
        return "Ship Not Found"


def get_ship_name(ship_id):
    """
    Searches the EvE database to resolve the name of a ship's ship_id

    :param ship_id: Ship_id of the ship to be looked up
    :return: The name of the ship_id specified
    """
    try:
        look_up_url = "https://esi.evetech.net/latest/" \
                      "universe/" \
                      "types/" + str(ship_id) + \
                      "/?datasource=tranquility&" \
                      "language=en-us"
        search_res = urllib.request.urlopen(look_up_url)
        data = json.loads(search_res.read().decode())
        return data["name"]
    except urllib.error.HTTPError:
        return "ESI Not Responding"
    except urllib.error.URLError:
        return "Ship Not Found"


def get_item_id(name):

    fixed_name = name.replace(" ", "%20")
    look_up_url = "https://esi.evetech.net/latest/" \
                  "search/" \
                  "?categories=inventory_type&" +\
                  "datasource=tranquility&" \
                  "language=en-us&" \
                  "search=" + fixed_name + \
                  "&strict=true"
    try:
        search_res = urllib.request.urlopen(look_up_url)
        data = json.loads(search_res.read().decode())
        return str((data["inventory_type"])).lstrip("[").rstrip("]")

    except urllib.error.HTTPError:
        return "ESI Not Responding"
    except urllib.error.URLError:
        return "Item Not Found"


