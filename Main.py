import asyncio
import datetime

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

online_time = datetime.datetime.now()

channel = discord.Object(id='449651065051283476')


# background fuel checker
async def fuelAlert():
    await bot.wait_until_ready()
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
async def upTime():
    await bot.say("Online for: " + str(datetime.datetime.now() - online_time))

# zkill related functions


@bot.command()
async def kills(*, corp_name):
    try:
        c_id = Esi.get_corp_id(corp_name)
        await bot.say(Zkbf.get_corp_current_month_stats(corp_name, c_id))
    except Esi.urllib.error.HTTPError:
        await bot.say("ESI Not Responding")
    except (Esi.urllib.error.URLError, KeyError):
        await bot.say("Corp Not Found")


@bot.command()
async def ships(amount: int, *, corp_name):
    try:
        c_id = Esi.get_corp_id(corp_name)
        await bot.say(Zkbf.get_killer_summary(amount, corp_name, c_id))
    except Esi.urllib.error.HTTPError:
        await bot.say("ESI Not Responding")
    except (Esi.urllib.error.URLError, KeyError):
        await bot.say("Corp Not Found")


@bot.command()
async def stats(*, corp_name):
    try:
        c_id = Esi.get_corp_id(corp_name)
        await bot.say(Zkbf.get_fleet_size_stats(corp_name, c_id))
    except Esi.urllib.error.HTTPError:
        await bot.say("ESI Not Responding")
    except (Esi.urllib.error.URLError, KeyError):
        await bot.say("Corp Not Found")


@bot.command()
async def rankings():
    await bot.say(bf.get_ranked_isk_killed())


@bot.command()
async def intel(*, corp_name):
    try:
        c_id = Esi.get_corp_id(corp_name)
        output = ""
        output += Zkbf.get_corp_current_month_stats(corp_name, c_id) + "\n"
        output += Zkbf.get_fleet_size_stats(corp_name, c_id) + "\n"
        output += Zkbf.get_killer_summary(5, corp_name, c_id) + "\n"
        await bot.say(output)
    except Esi.urllib.error.HTTPError:
        await bot.say("ESI Not Responding")
    except (Esi.urllib.error.URLError, KeyError):
        await bot.say("Corp Not Found")


@bot.command()
async def fit(ship: str, *, corp):
    try:
        c_id = Esi.get_corp_id(corp)
        s_id = Esi.get_item_id(ship)
        await bot.say(corp + "'s " + ship + ": " + Zkbf.get_last_fit(s_id, c_id))
    except Esi.urllib.error.HTTPError:
        await bot.say("ESI Not Responding")
    except (Esi.urllib.error.URLError, KeyError):
        await bot.say("Corp or Ship Not Found")


# market functions


@bot.command()
async def pc(*, a):
    await bot.say(Fzw.get_item_value(a))


@bot.command()
async def fuel():
    await bot.say(Fzw.get_fuel_prices())

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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("error")
        bot.send_message(channel, "Command Not Found")
        return


bot.run(token)
