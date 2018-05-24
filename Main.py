from discord.ext import commands

import BotFunctions as bf
import ESIFunctions as Esi
import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.Decl9w.3O1LF-B8UAxZGWupqPSYSiMJiMo'
bot = commands.Bot(command_prefix='!')


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
async def commands():
    print("printing commands")

    out = bf.const_command_text("kills X",
                                "Retrieve the total isk killed in wormholes by corp **X**" +
                                " Enter the full corp name, or corp ticker\n" +
                                "1 ESI lookup, 1 Zkill lookup")

    out += bf.const_command_text("ships X Y",
                                 "Retrieve the top ***X***" +
                                 " list of ships used this year by corp **Y** seen as attackers on killmails\n" +
                                 "2 ESI lookups, 1 Zkill lookup")

    out += bf.const_command_text("stats X",
                                 "Poke Calir to fill this in at some point\n" +
                                 "1 ESI lookup, 1 Zkill lookup")

    out += bf.const_command_text("intel X",
                                 "Poke Calir to fill this in at some point\n" +
                                 "2 ESI lookups, 3 Zkill lookups")

    await bot.say(out)


bot.run(token)
