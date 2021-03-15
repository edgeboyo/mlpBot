import discord
from discord.ext import commands
import random

def getDrinks():
    try:
        with open("drinks.txt", "r") as f:
            drinks = int(f.readline())
        print("Drank {} so far".format(drinks))
    except:
        putDrinks(0)
        return 0
    return drinks

def putDrinks(d):
    with open("drinks.txt", "w") as f:
        f.write(str(d))

class MLPBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$')
        self.drinks = 0
        self.curDrinks = None
        self.seas = None
        self.ep = None

bot = MLPBot()

@bot.event
async def on_ready():
    bot.drinks = getDrinks()
    print('Logged on as {0}!'.format(bot.user))

@bot.command()
async def rollEp(ctx, arg):
    pick = int(arg)
    if pick <= 0 or pick >= 10:
        ctx.send("That's not a valid season number, silly!")
        return
    if pick == 3:
        ep = random.randint(1, 13)
    else:
        ep = random.randint(1, 26)
    await ctx.send("You are going to watch season {} episode {}! Have fun!".format(pick, ep))
    bot.seas = pick
    bot.ep = ep
    bot.curDrinks = 0

@bot.command()
async def roll(ctx):
    pick = random.randint(1, 9)
    ep = None
    if pick == 3:
        ep = random.randint(1, 13)
    else:
        ep = random.randint(1, 26)
    await ctx.send("You are going to watch season {} episode {}! Have fun!".format(pick, ep))
    bot.seas = pick
    bot.ep = ep
    bot.curDrinks = 0

@bot.command()
async def watch(ctx, seas, ep):
    seas = int(seas)
    ep = int(ep)
    await ctx.send("You are going to watch season {} episode {}! Have fun!".format(seas, ep))
    bot.seas = seas
    bot.ep = ep
    bot.curDrinks = 0
    

@bot.command()
async def drink(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("Bottoms up! :tropical_drink:")
    bot.curDrinks = bot.curDrinks + 1

@bot.command()
async def finish(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("You finished watching season {} episode {}!!!".format(bot.seas, bot.ep))
    await ctx.send("During the episode you've drank {} drinks! Good luck waking up tomorrow!".format(bot.curDrinks))
    bot.drinks = bot.drinks + bot.curDrinks
    bot.curDrinks = None
    bot.seas = None
    bot.ep = None
    putDrinks(bot.drinks)

@bot.command()
async def stop(ctx):
    putDrinks(bot.drinks)
    await ctx.send("Okay :<. Bye bye!!! :cry:")
    await bot.logout()

if __name__ == "__main__":
    token = open("discord.token", "r").read()
    if token[-1] == '\n':
        token = token[:-1]
    bot.run(token)