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
    for c in corp_list:
        c_id = ESIFunctions.get_corp_id(c)
        temp = ZkillFunctions.get_corp_current_month_stats(c, c_id)
        outputs[str(c)] = str(temp)
        i = temp.find("Killed:__ ")
        j = temp.find(" isk")
        temp = temp[i+10:j]
        rankings[temp] = c

    for k in sorted(rankings, reverse=True):
        output += outputs[rankings[k]]
    return output