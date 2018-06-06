import asyncio
import datetime

import discord
from discord.ext import commands

import BotFunctions as bf
import ESIFunctions as Esi
import FuzzworksFunctions as Fzw
import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.Decl9w.3O1LF-B8UAxZGWupqPSYSiMJiMo'
bot = commands.Bot(command_prefix='!')

structures = {}
fuelTimers = {}


#generate fuel Report
def fuelStatus():
    output = ""
    now = datetime.datetime.now()
    for i in fuelTimers:
        temp = fuelTimers[i]
        output += "**" + i + ":** "
        delta = temp - now
        if delta.days < 1:
            output += "__Sub 1 Day of Fuel__: " + str(delta)[:8] + " remaining"
        else:
            output += "Days Remaining: " + str(delta.days) + "\n\n"
    return output

#async def fuel_counting():
#    await bot.wait_until_ready
#    channel = discord.Object(id='449651065051283476')
#    while not bot.is_closed:


#background fuel checker
async def fuelAlert():
    await bot.wait_until_ready()
    channel = discord.Object(id='449651065051283476')
    while not bot.is_closed():
        output = fuelStatus()
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
    if name not in structures:
        structures[name] = int(consumption)
        await bot.say("Structure: " + name + " added")
    else:
        await bot.say("This Structure already exists")


@bot.command()
async def updateStructure(name: str, consumption):
    if name in structures:
        structures[name] = int(consumption)
        await bot.say("Structure: " + name + " updated")
    else:
        await bot.say("This structure does not exist")


@bot.command()
async def listStructures():
    output = ""
    for i in structures:
        output += i + ": " + str(structures[i]) + "\n"
    await bot.say(output)


@bot.command()
async def addFuel(name: str, amount):
    if name in structures:
        daysRemaining = int(amount) / structures[name]
        now = datetime.datetime.now()
        unFueled = now + datetime.timedelta(days=daysRemaining)
        fuelTimers[name] = unFueled
        await bot.say("Structure: " + str(name) + "- Fuel level updated")
    else:
        await bot.say("This structure does not exist")


@bot.command()
async def fuelReport():
    await bot.say(fuelStatus())


@bot.command()
async def setUp():
    structures["astra"] = int(180)
    daysRemaining = int(100) / structures["astra"]
    now = datetime.datetime.now()
    unFueled = now + datetime.timedelta(days=daysRemaining)
    fuelTimers["astra"] = unFueled


@bot.command()
async def commands():
    print("printing commands")

    out = bf.const_command_text("kills X",
                                "Retrieve the total isk killed in wormholes by corp **X**" +
                                " Enter the full corp name, or corp ticker")

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


bot.run(token)
