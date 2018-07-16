import datetime
import sqlite3
from sqlite3 import Error


class FuelTracker:

    structures = {}  # list tracking structure name and structure consumption rate
    fuelTimers = {}  # list tracking structure name and fuel run out datetime

    DB = "Data/Structure_Data"

    sql_create_structures_table = """CREATE TABLE IF NOT EXISTS structures (
                                     name text PRIMARY KEY,
                                     consumption_rate integer NOT NULL,
                                     expiry_date real
                                     );"""

    def __init__(self):
        conn = create_connection(self.DB)
        if conn is not None:
            # create structures table
            create_table(conn, self.sql_create_structures_table)
            print("DB connected")
        else:
            print("Error, database not found")
        conn.close()

    def add_structure(self, name: str, consumption):
        """
        Adds structure to list of structures with it's consumption rate

        :param name: Identifier of structure
        :param consumption: Fuel blocks consumed per day (numbers only)
        :return: Status of structure addition
        """
        conn = create_connection(self.DB)
        # check if exists
        cur = conn.cursor()
        cur.execute("SELECT * FROM structures WHERE name=?",(name,))
        data = cur.fetchall()
        if len(data) == 0:
            # add structure to db
            cur = conn.cursor()
            cur.execute("INSERT INTO structures VALUES(?,?,?)", (name, int(consumption), None))
            conn.commit()
            conn.close()
            return "Structure: " + name + " added"
        else:
            return "This Structure Already Exists"

    def update_structure(self, name: str, consumption):
        """
        Updates an existing structure's fuel consumption rate

        :param name:  Identifier of Structure to update
        :param consumption:  New consumption rate of specified structure
        :return: Status of the structure update
        """
        if consumption == 0:
            return "Consumption rate must be > 0"
        try:
            conn = create_connection(self.DB)
            cur = conn.cursor()
            cur.execute("SELECT * FROM structures WHERE name=?", (name,))
            data = cur.fetchall()
            if len(data) == 0:  # no matching structure found
                return "Structure Not Found"
            elif len(data) == 1:  # structure found (once), updating
                cur = conn.cursor()
                cur.execute("UPDATE structures SET consumption_rate=?", (consumption,))
                conn.commit()
                conn.close()
                return "Structure: " + name + " Updated"
            elif len(data) > 1:  # structure found more than once?!?
                return "You have somehow cloned a structure, how in the hell did you manage that!"
        except ValueError:
                return "Consumption rate must be a number"

    def list_structures(self):
        """
        Generates a list of existing structures and their consumption rates

        :return: List of structures and consumption rates in format of: "structure name": "structure consumption rate"
        """
        conn = create_connection(self.DB)
        cur = conn.cursor()
        cur.execute("SELECT name, consumption_rate FROM structures")
        data = cur.fetchall()
        output = ""
        for structure in data:
            output += str(structure[0]) + ": "
            output += str(structure[1]) + "\n"
        return output

    def update_fuel(self, name: str, amount):
        """
        Update the current fuel level in a structure
        Calculate and store datetime specified structure will run out of fuel
        Store said datetime in FuelTimers

        :param name: Identifier of structure to update
        :param amount: Amount of fuel in fuel bay of specified structure
        :return:  Status of the fuel update
        """
        try:
            conn = create_connection(self.DB)
            cur = conn.cursor()
            cur.execute("SELECT * FROM structures WHERE name=?", (name,))
            data = cur.fetchall()
            if len(data) == 0:  # no matching structure found
                return "Structure Not Found"
            elif len(data) == 1:  # structure found (once), updating
                print("projecting")
                #  fuel projection
                days_remaining = int(amount) / data[0][1]
                now = datetime.datetime.now()
                un_fueled = now + datetime.timedelta(days=days_remaining)
                # store fuel expiry date
                print("writing")
                cur = conn.cursor()
                cur.execute("UPDATE structures SET expiry_date=?", (un_fueled,))
                conn.commit()
                conn.close()
                return "Structure: " + name + " Updated"
            elif len(data) > 1:  # structure found more than once?!?
                return "You have somehow cloned a structure, how in the hell did you manage that!"
        except ValueError:
                return "Fuel amount must be a number"

    def fuel_status(self):
        """
        Generate a list of existing structures and the fueled time remaining for each
        :return:  list of structures and fuel-out times in format of "structure name": "time remaining"
        """
        conn = create_connection(self.DB)
        cur = conn.cursor()
        cur.execute('SELECT name, date(expiry_date), time(expiry_date) FROM structures')
        data = cur.fetchall()
        output = ""
        now = datetime.datetime.now()
        for structure in data:
            print(structure)

            name = structure[0]
            print(name)
            temp = datetime.datetime.strptime(structure[1] + structure[2], "%Y-%m-%d%H:%M:%S")
            print(temp)
            output += "**" + name + ":** "
            delta = temp - now
            if delta.days < 1:
                output += "__Sub 1 Day of Fuel__: " + str(delta)[:8] + " remaining"
            else:
                output += "Days Remaining: " + str(delta.days) + "\n\n"
        if output == "":
            return "No structures Exist"
        else:
            return output


def create_connection(db_file):
    """
    Creates a database connection to SQLite database
    :param db_file: file to connect to
    :return: connection object or none
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """
    Create a table from the current_table_aql statement
    :param conn: connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
