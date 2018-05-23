import datetime
import json
import operator
import urllib.request
from collections import defaultdict

import ESIFunctions as Esi


def get_corp_current_month_stats(name):
    """
    Calculates the total number of corp member kills and value of said corp's kills within the current month.
    Retrieves the kill history for the current month and calculates total kills and total worth of said kills

    Current hard-coded filters:
        w-space only - because we only care about wormhole kills
        final-blow kills only - to limit kill-whoring skewing results

    :param name: The full corp name or corp ticker, to look up
    :return: Statistics string to be displayed
    """
    # construct Zkill Stat query
    print("Getting Corp Current Month Stats")
    kb_url = ("https://zkillboard.com/api/stats/corporationID/" +
             Esi.get_corp_id(name) + "/w-space/year/" +
             str(datetime.date.today().year) + "/month/" +
             str(datetime.date.today().month) + "/kills/finalblow-only/")
    # store zkill stat result
    kb_sum = urllib.request.urlopen(kb_url)

    # convert zkill output
    data = json.loads(kb_sum.read().decode())
    # initialise counters
    total_isk = 0
    total_kills = 0
    # for every kill in output
    for i in data:
        # add value of zkb object, totalValue to total
        total_isk += i["zkb"]["totalValue"]
        # increment totalKill counter
        total_kills += 1

    return (name + ":   Total Kills: " + str(total_kills) +
            "   Total Isk Killed: " + '{0:,.2f}'.format(total_isk))


def get_killer_summary(name, list_range):
    """
    Generates a list of the top "list_range" ships used in PvP by the specified corp.
    The kill history of a corp is requested from zkillboard, for the current year

    current hard-coded filters:
        w-space only - as we only care about wormhole space

    This is done via a frequency table constructed from attackers on each kill-mail, with a check that each pilot
    is within the target corporation

    :param name: The full corp name or corp ticker, to look up
    :param list_range: The maximum size of the returned list
    :return: Statistics string to be displayed
    """
    print("Getting Corp Killer Summary")
    id_set = []
    corp_id = Esi.get_corp_id(name)
    # construct Zkill Stat query
    kb_url = ("https://zkillboard.com/api/stats/corporationID/" + corp_id + "/w-space/year/"
              + str(datetime.date.today().year) + "/kills/")

    # store zkill stat result
    kb_sum = urllib.request.urlopen(kb_url)

    # convert zkill output
    data = json.loads(kb_sum.read().decode())

    # for every kill in output
    for i in data:
        # for every attacker
        for j in i["attackers"]:
            try:
                # check that attacker belongs to target corp
                if int(j["corporation_id"]) == int(corp_id):
                    id_set.append(j['ship_type_id'])
            except KeyError:
                print("KeyError")

    # print(id_set)
    freq_table = defaultdict(int)
    # for every type of ship in ship list
    for i in id_set:
        freq_table[i] += 1

    # construct matching arrays of ship IDs and Ship Frequencies
    ship_ids = []
    ship_count = []

    # clamp returned list size to specified value, or size of ship_ids - whichever is smaller
    list_size = 0
    if len(id_set) < list_range:
        list_size = len(id_set)
    else:
        list_size = list_range

    # for each item to be returned
    for i in range(list_size):
        # get ship_id of most popular ship in list
        current_id = max(freq_table.items(), key=operator.itemgetter(1))[0]
        # append ship_id and occurrence count to the lists
        ship_ids.append(current_id)
        ship_count.append(freq_table[current_id])
        # delete said ship_id from freq table so it isn't counted > once
        del freq_table[current_id]

    # add output header
    output = name + " - PvP Ship Summary:\n"
    # construct output string
    for i in range(len(ship_ids)):
        output += str(Esi.get_ship_name(ship_ids[i])) + ": " + str(ship_count[i]) + "\n"

    return output
