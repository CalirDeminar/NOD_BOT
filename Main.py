import asyncio

import discord
from discord.ext import commands

import BotFunctions as bf
import ESIFunctions as Esi
import FuelTracker
import FuzzworksFunctions as Fzw
import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.Decl9w.3O1LF-B8UAxZGWupqPSYSiMJiMo'
bot = commands.Bot(command_prefix='!')

fuel_tracker = FuelTracker.FuelTracker()


# background fuel checker
async def fuelAlert():
    await bot.wait_until_ready()
    channel = discord.Object(id='449651065051283476')
    while not bot.is_closed():
        output = fuel_tracker.fuel_status()
        bot.send_message(channel, output)
        await asyncio.sleep(3600)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping():
    await bot.say("pong")


@bot.command()
async def kills(*, a):
    c_id = Esi.get_corp_id(a)
    await bot.say(Zkbf.get_corp_current_month_stats(a, c_id))


@bot.command()
async def ships(a: int, *, b):
    c_id = Esi.get_corp_id(b)
    await bot.say(Zkbf.get_killer_summary(a, b, c_id))


@bot.command()
async def stats(*, a):
    c_id = Esi.get_corp_id(a)
    await bot.say(Zkbf.get_fleet_size_stats(a, c_id))


@bot.command()
async def rankings():
    await bot.say(bf.get_ranked_isk_killed())


@bot.command()
async def intel(*, a):
    c_id = Esi.get_corp_id(a)
    output = ""
    output += Zkbf.get_corp_current_month_stats(a, c_id) + "\n"
    output += Zkbf.get_fleet_size_stats(a, c_id) + "\n"
    output += Zkbf.get_killer_summary(5, a, c_id) + "\n"
    await bot.say(output)


@bot.command()
async def pc(*, a):
    await bot.say(Fzw.get_item_value(a))


@bot.command()
async def fuel():
    await bot.say(Fzw.get_fuel_prices())


@bot.command()
async def fit(ship: str, *, corp):
    c_id = Esi.get_corp_id(corp)
    s_id = Esi.get_item_id(ship)
    await bot.say(corp + "'s " + ship + ": " + Zkbf.get_last_fit(s_id, c_id))


# Fuel commands **********************************************


@bot.command()
async def addStructure(name: str, consumption):
    await bot.say(fuel_tracker.add_structure(name, consumption))


@bot.command()
async def updateStructure(name: str, consumption):
    await bot.say(fuel_tracker.update_structure(name, consumption))


@bot.command()
async def listStructures():
    await bot.say(fuel_tracker.list_structures())


@bot.command()
async def updateFuel(name: str, amount):
    await bot.say(fuel_tracker.update_fuel(name, amount))


@bot.command()
async def fuelReport():
    await bot.say(fuel_tracker.fuel_status())


@bot.command()
async def setUp():
    fuel_tracker.add_structure("astra", 180)
    fuel_tracker.add_structure("fort", 320)


@bot.command()
async def commands():
    print("printing commands")

    out = bf.const_command_text("kills X",
                                "Retrieve the total isk killed in wormholes by corp **X**" +
                                " Enter the full corp name, or corp ticker")

    out += bf.const_command_text("rankings",
                                 "Get listing of familiar corps kill totals this month")

    out += bf.const_command_text("ships X Y",
                                 "Retrieve the top ***X***" +
                                 " list of ships used this year by corp **Y** seen as attackers on killmails")

    out += bf.const_command_text("fit X Y",
                                 "Retrieve the last killmail of ship **X** from corp **Y**")

    out += bf.const_command_text("stats X",
                                 "Retrieve fleet size statistics for corp **X**")

    out += bf.const_command_text("intel X",
                                 "Combined command to call: kills, stats and ships commands")

    out += bf.const_command_text("pc X", "Price check item X at Jita 4-4\n1 ESI lookup, 1 Fuzzworks lookup")

    out += bf.const_command_text("fuel", "Gets prices of all fuel blocks from amarr and jita")

    await bot.say(out)

while True:
    bot.run(token)
