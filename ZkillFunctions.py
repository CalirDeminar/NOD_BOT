import datetime
import json
import math
import operator
import urllib.error
import urllib.request
from collections import defaultdict

import ESIFunctions as Esi

DB = "Data/Structure_Data"





def get_corp_current_month_stats(name):
    """ ******FIXED******
    Calculates the total number of corp member kills and value of said corp's kills within the current month.
    Retrieves the kill history for the current month and calculates total kills and total worth of said kills

    Current hard-coded filters:
        w-space only - because we only care about wormhole kills
        final-blow kills only - to limit kill-whoring skewing results

    :param name: The full corp name or corp ticker, to look up
    :return: Statistics string to be displayed
    """
    # construct Zkill Stat query
    try:
        corp_id = Esi.get_corp_id(name)
    except Esi.urllib.error.HTTPError:
        return "ESI Not Responding"
    except (Esi.urllib.error.URLError, KeyError):
        return "Corp Not Found"
    now = datetime.date.today()
    try:
        print("Getting Corp Current Month Stats")
        kb_url = "https://zkillboard.com/api/" \
                 "corporationID/" + corp_id + \
                 "/w-space/" \
                 "startTime/" + str(now.year) + str('{:02d}'.format(now.month)) + "000000" \
                 "/kills/finalblow-only/"
        print(kb_url)
        # store zkill stat result
        kb_sum = urllib.request.urlopen(kb_url)
        # convert zkill output
        data = json.loads(kb_sum.read().decode())
        # initialise counters
        total_isk = 0
        total_kills = 0
        # for every kill in output
        for kill in data:
            # add value of zkb object, totalValue to total
            total_isk += kill["zkb"]["totalValue"]
            # increment totalKill counter
            total_kills += 1

        return "__**" + name + \
               ":**__   __Total Kills:__ " + str(total_kills) + \
               "   __Total Isk Killed:__ " + '{0:,.2f}'.format(total_isk) + \
               " isk\n"
    except TypeError:
        return "**LookUp Error**"
    except urllib.error.HTTPError:
        return "Zkill Not Responding"


def get_killer_summary(list_range, name):
    """ ****** NOT DONE ******
    Generates a list of the top "list_range" ships used in PvP by the specified corp.
    The kill history of a corp is requested from zkillboard, for the current year

    current hard-coded filters:
        w-space only - as we only care about wormhole space

    This is done via a frequency table constructed from attackers on each kill-mail, with a check that each pilot
    is within the target corporation

    :param list_range: The maximum size of the returned list
    :param name: The full corp name or corp ticker, to look up
    :return: Statistics string to be displayed
    """
    try:
        corp_id = Esi.get_corp_id(name)
    except Esi.urllib.error.HTTPError:
        return "ESI Not Responding"
    except (Esi.urllib.error.URLError, KeyError):
        return "Corp Not Found"

    try:
        print("Getting Corp Killer Summary")
        id_set = []
        # construct Zkill Stat query
        kb_url = "https://zkillboard.com/api/" + \
                 "corporationID/" + corp_id + \
                 "/w-space/" + \
                 "year/" + str(datetime.date.today().year) + \
                 "/kills/"

        # store zkill stat result
        kb_sum = urllib.request.urlopen(kb_url)
        # convert zkill output
        data = json.loads(kb_sum.read().decode())

        # for every kill in output
        for kill in data:
            # for every attacker
            print("per kill")
            print(kill)
            print(kill.killmail_id)
            print(kill.zkb.hash)
            killmail = Esi.get_km(kill.killmail_id, kill.zkb.hash)
            print("killmail got")
            for attacker in killmail["attackers"]:
                try:
                    # check that attacker belongs to target corp
                    if int(attacker["corporation_id"]) == int(corp_id):
                        id_set.append(attacker['ship_type_id'])
                except KeyError:
                    print("KeyError")

        # print(id_set)
        freq_table = defaultdict(int)
        # for every type of ship in ship list
        for ship_id in id_set:
            freq_table[ship_id] += 1

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
        output = "__**" + name + \
                 " - PvP Ship Summary:**__\n"
        # construct output string
        for i in range(len(ship_ids)):
            output += str(Esi.get_ship_name(ship_ids[i])) + ": " + str(ship_count[i]) + "\n"
        return output

    except TypeError:
        return "**LookUp Error**"
    except urllib.error.HTTPError:
        return "Zkill Not Responding"


def get_fleet_size_stats(name):
    """
    Calculates fleet size statistics for a specified corp ID
    Checks number of specified corp_members of each corp kill
    Corp kills are discarded if < 50% of attackers on killmail are not from specified corp

    Calculates Max, Min and Avg fleet sizes of target corp


    :param name: Corp name to be contained in output string (passed so ESI doesnt have to be called)
    :return: Output String to be displayed
    """
    try:
        corp_id = Esi.get_corp_id(name)
    except Esi.urllib.error.HTTPError:
        return "ESI Not Responding"
    except (Esi.urllib.error.URLError, KeyError):
        return "Corp Not Found"

    print("Getting Fleet Size Stats")
    try:
        # construct Zkill Stat query
        kb_url = "https://zkillboard.com/api/" + \
                 "corporationID/" + corp_id + \
                 "/w-space/" + \
                 "year/" + str(datetime.date.today().year) + \
                 "/kills/"

        # store zkill stat result
        kb_sum = urllib.request.urlopen(kb_url)
        # convert zkill output
        data = json.loads(kb_sum.read().decode())

        avg_total = 0
        total_kills = 0
        max_k = 0
        min_k = math.inf

        for kill in data:  # for every kill
            current_total = 0
            third_pty = 0
            for attacker in kill["attackers"]:  # for every attacker
                try:
                    if int(attacker["corporation_id"]) == int(corp_id):  # increment only if attack is of target corp
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

        # construct output string
        output = "__**Fleet Statistics:**__\n"
        output += "__Maximum Fleet Size:__  " + str(max_k) + "\n"
        output += "__Minimum Fleet Size:__  " + str(min_k) + "\n"
        output += "__Average Fleet Size:__  " + str('{0:,.2f}'.format(avg)) + "\n"
        output += "__Sample Size:__ " + str(total_kills) + "\n"
        return output
    except KeyError:
        return "**LookUp Error**"
    except urllib.error.HTTPError:
        return "Zkill Not Responding"


def get_intel(name):
    """
    Macro function of get_corp_current_month_stats
                      get_fleet_size_stats and
                      get_killer_summary
    :param name: corp name to look up
    :return:  output string to be printed
    """
    output = ""
    output += get_corp_current_month_stats(name) + "\n"
    if output == "Corp Not Found\n":
        return output
    output += get_fleet_size_stats(name) + "\n"
    output += get_killer_summary(5, name) + "\n"
    return output


def get_last_fit(ship, name):
    """
    Generate a zkillboard link to the last of the specified ship from the specified corp
    :param ship: Name of ship to search for
    :param name: Corp name to limit search within
    :return: Zkillboard killmail URL
    """
    try:
        corp_id = Esi.get_corp_id(name)
    except Esi.urllib.error.HTTPError:
        return "ESI Not Responding"
    except (Esi.urllib.error.URLError, KeyError):
        return "Corp Not Found"
    try:
        ship_id = Esi.get_item_id(ship)
    except Esi.urllib.error.HTTPError:
        return "ESI Not Responding"
    except (Esi.urllib.error.URLError, KeyError):
        return "Ship Not Found"
    try:
        print("getting corp's ship fit")
        # construct Zkill Stat query
        kb_url = "https://zkillboard.com/api/" + \
                 "corporationID/" + corp_id + \
                 "/w-space/" + \
                 "year/" + str(datetime.date.today().year) + \
                 "/losses/shipID/" + ship_id + "/"

        print(kb_url)
        # store zkill stat result
        kb_sum = urllib.request.urlopen(kb_url)
        # convert zkill output
        data = json.loads(kb_sum.read().decode())
        kill_id = data[0]["killmail_id"]
        return name + "'s " + ship + ": https://zkillboard.com/kill/" + str(kill_id) + "/"
    except KeyError:
        return "**LookUp Error**"
    except urllib.error.HTTPError:
        return "Zkill Not Responding"


