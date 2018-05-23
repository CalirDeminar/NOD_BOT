import discord
from discord.ext import commands

import ZkillFunctions as Zkbf

token = 'NDQ4ODU2MTExNjcyNTkwMzQ3.DecXXQ.571MSQN-E6eMpBCTX_hCVb_ZRxg'
bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def get_corp_monthly(a):
    await bot.say(Zkbf.get_corp_current_month_stats(a))


@bot.command()
async def corp_look_up(a: str, b: int):
    await bot.say(Zkbf.get_killer_summary(a, b))


@bot.command()
async def commands():
    embed = discord.Embed(title="NOD_BOT", description="NOD Utility Bot", color=0xeee657)

    embed.add_field(name="", value="", inline=False)

    embed.add_field(name="#get_corp_monthly **X**", value="Retrieve the total isk killed in wormholes by corp **X**"
                                                          "Enter the full corp name, or corp ticker", inline=False)

    embed.add_field(name="#corp_look_up **X Y **", value="Retrieve the top ***Y*** list of ships"
                                                         "used this year by corp **X**", inline=False)

    await bot.say(embed=embed)

bot.run(token)
