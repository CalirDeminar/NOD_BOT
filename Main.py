#!/usr/bin/python3
import asyncio
import datetime

import discord
from discord.ext import commands

import BotFunctions as bf
import FuelTracker
import FuzzworksFunctions as Fzw
import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.Decl9w.3O1LF-B8UAxZGWupqPSYSiMJiMo'
bot = commands.Bot(command_prefix='!')

fuel_tracker = FuelTracker.FuelTracker()

online_time = datetime.datetime.now()

# bot channel ID
channel = discord.Object(id='449651065051283476')


alertRunning = False


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')




@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def upTime(ctx):
    await ctx.send("Online for: " + str(datetime.datetime.now() - online_time))

# zkill related functions


@bot.command()
async def kills(ctx, *, corp_name):
    await ctx.send(Zkbf.get_corp_current_month_stats(corp_name))


@bot.command()
async def ships(ctx, amount: int, *, corp_name):
    await ctx.send(Zkbf.get_killer_summary(amount, corp_name))


@bot.command()
async def stats(ctx, *, corp_name):
    await ctx.send(Zkbf.get_fleet_size_stats(corp_name))


@bot.command()
async def rankings(ctx):
    await ctx.send(bf.get_ranked_isk_killed())


@bot.command()
async def intel(ctx, *, corp_name):
    await ctx.send(Zkbf.get_intel(corp_name))


@bot.command()
async def fit(ctx, ship: str, *, corp):
    await ctx.send(Zkbf.get_last_fit(ship, corp))


# market functions


@bot.command()
async def pc(ctx, *, a):
    await ctx.send(Fzw.get_item_value(a))


@bot.command()
async def fuel(ctx):
    await ctx.send(Fzw.get_fuel_prices())

# Fuel commands **********************************************


@bot.command()
async def addStructure(ctx, name: str, consumption):
    await ctx.send(fuel_tracker.add_structure(name, consumption))


@bot.command()
async def updateStructure(ctx, name: str, consumption):
    await ctx.send(fuel_tracker.update_structure(name, consumption))


@bot.command()
async def listStructures(ctx):
    await ctx.send(fuel_tracker.list_structures())


@bot.command()
async def updateFuel(ctx, name: str, amount):
    await ctx.send(fuel_tracker.update_fuel(name, amount))


@bot.command()
async def fuelReport(ctx):
    await ctx.send(fuel_tracker.fuel_status())


# background fuel checker
@bot.command()
@commands.has_role("Director")
async def fuelAlert(ctx):
    while True:

        output = fuel_tracker.fuel_status()
        await ctx.send(output)

        now = datetime.datetime.now()
        target_time = datetime.timedelta(microseconds=-now.microsecond,
                                         seconds=-now.second,
                                         minutes=-now.minute,
                                         hours=15 - now.hour)
        if now.hour > 15:
            target_time += datetime.timedelta(days=1)

        await asyncio.sleep(target_time.seconds)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("error")
        bot.send_message(channel, "Command Not Found")
        return


bot.run(token)
