import datetime
import json
import math
import operator
import urllib.request
from collections import defaultdict

import ESIFunctions as Esi


def get_corp_current_month_stats(name, corp_id):
    """
    Calculates the total number of corp member kills and value of said corp's kills within the current month.
    Retrieves the kill history for the current month and calculates total kills and total worth of said kills

    Current hard-coded filters:
        w-space only - because we only care about wormhole kills
        final-blow kills only - to limit kill-whoring skewing results

    :param name: The full corp name or corp ticker, to look up
    :param corp_id:
    :return: Statistics string to be displayed
    """
    # construct Zkill Stat query
    try:
        print("Getting Corp Current Month Stats")
        kb_url = ("https://zkillboard.com/api/stats/corporationID/" +
                  corp_id + "/w-space/year/" +
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

        return ("__**" + name + ":**__   __Total Kills:__ " + str(total_kills) +
                "   __Total Isk Killed:__ " + '{0:,.2f}'.format(total_isk) + " isk\n")
    except TypeError:
        return "**LookUp Error**"


def get_killer_summary(list_range, name, corp_id):
    """
    Generates a list of the top "list_range" ships used in PvP by the specified corp.
    The kill history of a corp is requested from zkillboard, for the current year

    current hard-coded filters:
        w-space only - as we only care about wormhole space

    This is done via a frequency table constructed from attackers on each kill-mail, with a check that each pilot
    is within the target corporation

    :param list_range: The maximum size of the returned list
    :param name: The full corp name or corp ticker, to look up
    :param corp_id:
    :return: Statistics string to be displayed
    """
    try:
        print("Getting Corp Killer Summary")
        id_set = []
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
        output = "__**" + name + " - PvP Ship Summary:**__\n"
        # construct output string
        for i in range(len(ship_ids)):
            output += str(Esi.get_ship_name(ship_ids[i])) + ": " + str(ship_count[i]) + "\n"

        return output
    except TypeError:
        return "**LookUp Error**"


def get_fleet_size_stats(name, corp_id):
    print("Getting Fleet Size Stats")
    try:
        # construct Zkill Stat query
        kb_url = ("https://zkillboard.com/api/stats/corporationID/" + corp_id + "/w-space/year/"
                  + str(datetime.date.today().year) + "/kills/")

        # store zkill stat result
        kb_sum = urllib.request.urlopen(kb_url)
        # convert zkill output
        data = json.loads(kb_sum.read().decode())

        avg_total = 0
        total_kills = 0
        max_k = 0
        min_k = math.inf

        for i in data:  # for every kill
            current_total = 0
            third_pty = 0
            for j in i["attackers"]:  # for every attacker
                try:
                    if int(j["corporation_id"]) == int(corp_id):  # increment only if attack is of target corp
                        current_total += 1
                    else:  # otherwise increment non-corp attacker counter
                        third_pty += 1
                except KeyError:
                    print("KeyError")
            if current_total > third_pty:  # ignore any kill with more non-corp attackers, than corp attacks
                if current_total > max_k:  # check and set new max fleet size
                    max_k = current_total
                elif current_total < min_k:  # check and set new min fleet size
                    min_k = current_total

                avg_total += current_total  # add to running total for mean fleet size
                total_kills += 1

        avg = avg_total / total_kills  # calculate mean fleet size

        output = "__**Fleet Statistics:**__\n"
        output += "__Maximum Fleet Size:__  " + str(max_k) + "\n"
        output += "__Minimum Fleet Size:__  " + str(min_k) + "\n"
        output += "__Average Fleet Size:__  " + str('{0:,.2f}'.format(avg)) + "\n"
        output += "__Sample Size:__ " + str(total_kills) + "\n"
        return output
    except KeyError:
        return "**LookUp Error**"

