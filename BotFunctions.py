import datetime
import re
import sqlite3

import ZkillFunctions as Zkbf

DB = "Data/Structure_Data"


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


def roll_out_init():
    """
    Check database connection and initialise rollOut table if not exists
    :return: None
    """
    sql_create_table = """CREATE TABLE IF NOT EXISTS rollOut (
                          date real PRIMARY KEY,
                          name text NOT NULL);"""
    conn = sqlite3.connect(DB)
    if conn is not None:
        # create structures table
        c = conn.cursor()
        c.execute(sql_create_table)
        print("DB connected")
    else:
        print("Error, database not found")
    conn.close()


def get_rolled_out_date():
    """
    Get the last rolled out date
    :return: most recent rolled out date
    """
    # connect DB
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT date(date)"
                "FROM rollOut "
                "ORDER BY date DESC "
                "LIMIT 1")
    data = cur.fetchall()
    conn.close()
    print(str(data[0]))
    temp = datetime.datetime.strptime(str(data[0]), "('%Y-%m-%d',)")
    delta = datetime.datetime.now() - temp
    return "Days Since Last RollOut: " + str(delta.days)


def update_rolled_out(name: str):
    """
    Add new rolled out entry with current time
    :param name: name of pilot rolled out
    :return: conformation of entry posting string
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    now = datetime.datetime.now()
    cur.execute("INSERT INTO rollOut "
                "VALUES (?,?)", (now, name))
    conn.commit()
    conn.close()
    return "RollOut Clock Reset"

