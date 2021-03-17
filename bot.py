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
        self.watcher.getWatcher()

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
    await ctx.send("TODO Add funny comment (double)")
    bot.curDrinks = bot.curDrinks + 2

@bot.command()
async def triple(ctx):
    if bot.seas == None:
        await ctx.send("You're not watching anything now!!!! :angry:")
        return
    await ctx.send("TODO Add funny comment (triple)")
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
    remmes = await ctx.send("This can take a moment...")
    await ctx.send("Current episode tally is:")
    lines = s.split("\n")
    for i in lines:
        if len(i) > 0:
            await ctx.send(i)
    await ctx.send("You idiots drank {} shots of alcohol :tumbler_glass:. Happy Liver Cancer!!! :100::100::100:".format(bot.drinks))
    await remmes.delete()

@bot.command()
async def unwatch(ctx, seas, ep):
    try:
        seas = int(seas)
        ep = int(ep)
        if not bot.watcher.series[seas][ep]:
            ctx.send("You haven't watched this yet... :smiling_face_with_tear:")
            return
        bot.watcher.series[seas][ep] = False
    except:
        ctx.send("I don't think that's an episode... :cry:")
        return
    ctx.send("You can expierience S{}E{} again".format(seas, ep))

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