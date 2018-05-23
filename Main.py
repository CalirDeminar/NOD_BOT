from discord.ext import commands

import BotFunctions as bf
import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.Decl9w.3O1LF-B8UAxZGWupqPSYSiMJiMo'
bot = commands.Bot(command_prefix='£')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def kills(*, a):
    await bot.say(Zkbf.get_corp_current_month_stats(str(a)))


@bot.command()
async def ships(a: int, *, b):
    await bot.say(Zkbf.get_killer_summary(a, b))


@bot.command()
async def commands():
    print("printing commands")

    out = bf.const_command_text("kills X",
                                "Retrieve the total isk killed in wormholes by corp **X**" +
                                " Enter the full corp name, or corp ticker")

    out += bf.const_command_text("ships X Y",
                                 "Retrieve the top ***X***" +
                                 " list of ships used this year by corp **Y** seen as attackers on killmails")

    await bot.say(out)


bot.run(token)
