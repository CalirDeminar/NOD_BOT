import re

import ZkillFunctions as Zkbf


def get_ranked_isk_killed():
    """
    Get amount of isk killed by list of corps
    Sort list of corps by amount killed
    :return: ordered string of corps and amount killed this month, to display
    """
    corp_list = ["Mass Collapse",
                 "Nothing On D",
                 "Interstellar Nuclear Penguins",
                 "Mind Collapse",
                 "Hole Awareness"]

    output = ""

    rankings = {}
    outputs = {}
    for corp_name in corp_list:
        temp = Zkbf.get_corp_current_month_stats(corp_name)
        outputs[str(corp_name)] = str(temp)
        sub_string_start = temp.find("Killed:__ ")
        sub_string_end = temp.find(" isk")
        temp = float(re.sub(',', '', temp[sub_string_start+10:sub_string_end]))
        rankings[temp] = corp_name

    for item in sorted(rankings, reverse=True):
        output += outputs[rankings[item]] + "\n"
    return output
