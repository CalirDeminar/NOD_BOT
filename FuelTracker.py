import datetime


class FuelTracker:

    structures = {}  # list tracking structure name and structure consumption rate
    fuelTimers = {}  # list tracking structure name and fuel run out datetime

    def add_structure(self, name: str, consumption):
        """
        Adds structure to list of structures with it's consumption rate

        :param name: Identifier of structure
        :param consumption: Fuel blocks consumed per day (numbers only)
        :return: Status of structure addition
        """
        try:
            if name not in self.structures:
                self.structures[name] = int(consumption)
                return "Structure: " + name + " added"
            else:
                return "This Structure already exists"
        except ValueError:
                return "Consumption rate must be a number"

    def update_structure(self, name: str, consumption):
        """
        Updates an existing structure's fuel consumption rate

        :param name:  Identifier of Structure to update
        :param consumption:  New consumption rate of specified structure
        :return: Status of the structure update
        """
        try:
            if name in self.structures:
                self.structures[name] = int(consumption)
                return "Structure: " + name + " updated"
            else:
                return "This structure does not exist"
        except ValueError:
                return "Consumption rate must be a number"

    def list_structures(self):
        """
        Generates a list of existing structures and their consumption rates

        :return: List of structures and consumption rates in format of: "structure name": "structure consumption rate"
        """
        output = ""
        for i in self.structures:
            output += i + ": " + str(self.structures[i]) + "\n"
        return output

    def update_fuel(self, name: str, amount):
        """
        Update the current fuel level in a structure
        Calculate and store datetime specified structure will run out of fuel
        Store said datetime in FuelTimers

        :param name: Identifier of structure to update
        :param amount: Amount of fuel in fuel bay of specified structure
        :return:  Satus of the fuel update
        """
        try:
            if name in self.structures:
                days_remaining = int(amount) / self.structures[name]
                now = datetime.datetime.now()
                un_fueled = now + datetime.timedelta(days=days_remaining)
                self.fuelTimers[name] = un_fueled
                return "Structure: " + str(name) + "- Fuel level updated"
            else:
                return "This structure does not exist"
        except ValueError:
                return "Fuel amount must be a number"

    def fuel_status(self):
        """
        Generate a list of existing structures and the fueled time remaining for each
        :return:  list of structures and fuel-out times in format of "structure name": "time remaining"
        """
        output = ""
        now = datetime.datetime.now()
        for i in self.fuelTimers:
            temp = self.fuelTimers[i]
            output += "**" + i + ":** "
            delta = temp - now
            if delta.days < 1:
                output += "__Sub 1 Day of Fuel__: " + str(delta)[:8] + " remaining"
            else:
                output += "Days Remaining: " + str(delta.days) + "\n\n"
        return output
