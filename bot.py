import inspect
import discord
from discord.ext import commands
from series import WatchTimeHolder
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
        self.watcher = WatchTimeHolder()

bot = MLPBot()

bot.remove_command('help')

@bot.event
async def on_ready():
    bot.drinks = getDrinks()
    bot.watcher.getWatcher()
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
    await ctx.send("You are going to watch season **{}** episode **{}**! Have fun!".format(pick, ep))
    bot.seas = pick
    bot.ep = ep
    bot.curDrinks = 0

@bot.command()
async def roll(ctx):
    sel = bot.watcher.roll()
    if isinstance(sel, str):
        await ctx.send(sel)
        return
    pick = sel[0]
    ep = sel[1]
    await ctx.send("You are going to watch season **{}** episode **{}**! Have fun!".format(pick, ep))
    bot.seas = pick
    bot.ep = ep
    bot.curDrinks = 0

@bot.command()
async def watch(ctx, seas, ep):
    seas = int(seas)
    ep = int(ep)
    await ctx.send("You are going to watch season **{}** episode **{}**! Have fun!".format(seas, ep))
    bot.seas = seas
    bot.ep = ep
    bot.curDrinks = 0
    
@bot.command()
async def blackout(ctx):
    await ctx.send("OwO You couldn't cut it!!! Stopping ✨watch mode✨ :weary:")
    bot.seas = None
    bot.ep = None
    bot.curDrinks = None

@bot.command()
async def drink(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("Bottoms up! :tropical_drink:")
    bot.curDrinks = bot.curDrinks + 1

@bot.command()
async def double(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("Too good to handle!! :champagne_glass: ")
    bot.curDrinks = bot.curDrinks + 2

@bot.command()
async def triple(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("Hat-trick!!! :beer: :beers: ")
    bot.curDrinks = bot.curDrinks + 3

@bot.command()
async def finish(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("You finished watching season **{}** episode **{}**!!!".format(bot.seas, bot.ep))
    await ctx.send("During the episode you've drank **{}** drinks! Good luck waking up tomorrow!".format(bot.curDrinks))
    bot.watcher.watch(bot.seas, bot.ep)
    bot.drinks = bot.drinks + bot.curDrinks
    bot.curDrinks = None
    bot.seas = None
    bot.ep = None
    putDrinks(bot.drinks)

@bot.command()
async def resetDrinks(ctx):
    bot.drinks = 0
    await ctx.send("Resetting drinks to 0...")

@bot.command()
async def resetWatches(ctx):
    bot.watcher = WatchTimeHolder()
    await ctx.send("Resetting watches to 0...")

@bot.command()
async def ruleset(ctx):
    s = "```Zasady MLPiekło\n\
        1. Gdy Spike pojawia się na ekranie – pijesz (1 szot);\n\
        2. Jak Pinkie Pie rozwala prawa fizyki lub logiki – pijesz (1 szot);\n\
        3. Jak Fluttershy powie zdanie dłuższe niż 5 słów – pijesz (2 szoty);\n\
        4. Jak Twilight Sparkle szaleje lub panikuje bez powodu – pijesz (1 szot);\n\
        5. Gdy Rainbow Dash zrobi coś głupiego i za to przeprosi – pijesz (1 szot);\n\
        6. Jak Rarity upada na szezlong (kozetkę) lub mdleje – pijesz (1 szot);\n\
        7. Jak Apple Jack wspomina o rodzinie  - pijesz (1 szot);\n\
        8. Jeśli jest piosenka (intro się nie liczy) – pijesz (3 szoty);\
    ```"
    await ctx.send(s)

@bot.command()
async def watchpage(ctx): 
    s = bot.watcher.craftMessage()
    p1 = "```Current episode tally is:\n" + s[0] + "\n"
    p2 = s[1] + "You idiots drank {} shots of alcohol 🥃 Happy Liver Cancer!!! 💯💯💯".format(bot.drinks) + "```"
    await ctx.message.delete()
    await ctx.send(p1 + p2)

@bot.command()
async def unwatch(ctx, seas, ep):
    try:
        seas = int(seas)
        ep = int(ep)
        if not bot.watcher.series[seas][ep]:
            await ctx.send("You haven't watched this yet... :smiling_face_with_tear:")
            return
        bot.watcher.series[seas][ep] = False
    except:
        await ctx.send("I don't think that's an episode... :cry:")
        return
    await ctx.send("You can experience S{}E{} again".format(seas, ep))

@bot.command()
async def help(ctx):
    await ctx.send("I can't help you, but if you want to operate me better go to: https://edgeboyo.github.io/mlpBot/ :wrench: ")

@bot.command()
async def stop(ctx):
    putDrinks(bot.drinks)
    bot.watcher.putWatcher()
    await ctx.send("Okay :<. Bye bye!!! :cry:")
    await bot.logout()

if __name__ == "__main__":
    token = open("discord.token", "r").read()
    if token[-1] == '\n':
        token = token[:-1]
    bot.run(token)