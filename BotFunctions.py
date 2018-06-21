import re

import ESIFunctions
import ZkillFunctions


def const_command_text(title, description):
    return "__**!" + title + "**__\n" + description + "\n\n"


def get_ranked_isk_killed():
    corp_list = ["Mass Collapse",
                 "Nothing On D",
                 "Interstellar Nuclear Penguins",
                 "Mind Collapse",
                 "Hole Awareness"]

    output = ""

    rankings = {}
    outputs = {}
    for corp_name in corp_list:
        c_id = ESIFunctions.get_corp_id(corp_name)
        temp = ZkillFunctions.get_corp_current_month_stats(corp_name, c_id)
        outputs[str(corp_name)] = str(temp)
        sub_string_start = temp.find("Killed:__ ")
        sub_string_end = temp.find(" isk")
        temp = float(re.sub(',', '', temp[sub_string_start+10:sub_string_end]))
        rankings[temp] = corp_name

    for item in sorted(rankings, reverse=True):
        output += outputs[rankings[item]] + "\n"
    return output
