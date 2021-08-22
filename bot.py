import asyncio
import codecs
import string
from random import randint
import datetime
from blagues_api import BlaguesAPI
from discord.ext import commands
import discord
from discord.utils import get
from tokenBot import TOKEN

blagues = BlaguesAPI(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjAwMjI3ODAzMTg5MjE1MjMyIiwibGltaXQiOjEwMCwia2V5IjoiY0NZe"
    "VRxb2lYVmE3dFpZYnhpQnBXbWpRalRha3VtMjNiN1A0SkVWU2dOeHY0WDF6MmYiLCJjcmVhdGVkX2F0IjoiMjAyMS0wNi0xNlQxOTowMjoyMys"
    "wMDowMCIsImlhdCI6MTYyMzg3MDE0M30.3Pq_NdS_220fpKHp-sPzWE-pYoMnarOi0gQ0tLF9zBI"
)

bot = commands.Bot(command_prefix='>')
table = str.maketrans(dict.fromkeys(string.punctuation))

helptxt = """
```
>blague [catégorie]         Catégories : dark, blondes, beauf, dev, global, limit
>e                          Encode un message/image
>d                          Décode un message encodé
>clear <nombre>             Clear x messages
>tg <@personne> <secondes>  Snipe un fdp pour lui faire fermer sa grosse gueule
```
"""


@bot.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(bot))


@bot.command(pass_context=True)
async def say(ctx):
    message = ctx.message
    if message.author.id == 200227803189215232:
        await message.delete()
        if len(message.content.split(' ')) == 1:
            await ctx.send(message.attachments[0].url)
        else:
            await ctx.send(' '.join(message.content.split(' ')[1:]))
    else:
        await ctx.send("hehe")


@bot.command(pass_context=True)
async def clear(ctx):
    message = ctx.message
    if message.author.id == 200227803189215232:
        limit_list = message.content.lower().split(" ")
        if len(limit_list) > 1:
            await ctx.channel.purge(limit=int(limit_list[1]))
        else:
            await ctx.send("Utilisation : >clear nombre")
    else:
        await ctx.send("hehe")


@bot.command(pass_context=True)
async def blague(ctx):
    arg = ctx.message.content.lower().split(" ")[1:]
    if ctx.channel.id == 851408106977230848:
        try:
            if len(arg) > 0:
                b = await blagues.random_categorized(arg[0])
            else:
                b = await blagues.random()
            await ctx.send(b.joke)
            await asyncio.sleep(3)
            await ctx.send(b.answer)
        except:
            await ctx.send(
                "Catégorie invalide mon reuf, essaye de taper `>aide` pour avoir toutes les catégories")


@bot.command(pass_context=True)
async def aide(ctx):
    await ctx.send(helptxt)

@bot.command(pass_context=True)
async def so(ctx):
    channel = bot.get_channel(667053408636633088)
    await channel.send(" ".join(ctx.message.content.split()[1:]))

@bot.command(pass_context=True)
async def tg(ctx, user: discord.Member, time: int):
    if ctx.message.author.guild_permissions.administrator or ctx.author.id == 200227803189215232:
        role = get(ctx.guild.roles, id=676415527098384406)
        await ctx.message.delete()
        await user.add_roles(role)
        await ctx.send(f"{ctx.author.name} a mute {user.name} pendant {time} secondes")
        await asyncio.sleep(time)
        await user.remove_roles(role)
    else:
        await ctx.send("Padpo pas les perms")

@bot.event
async def on_message(message):
    if message.channel.id == 876797710374682654:
        return
    if message.channel.id != 798877440607780954:
        chan = bot.get_channel(876797710374682654)
        embed = discord.Embed(title=f"#{message.channel.name}", colour=message.author.color, description=f"{message.content}", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{message.author.nick} ({message.author.name})", icon_url=message.author.avatar_url)
        try:
            embed.set_image(url=message.attachments[0].url)
        except:
            pass
        await chan.send(embed=embed)

    # MISC
    await bot.process_commands(message)
    msg = message.content.lower()

    if msg.startswith("envoie roux") or msg.startswith("sale roux"):
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/667053408636633088/821064431847866398/alors-toi-le-roukmout.mp4")
        return

    # ROT13
    if message.channel.id == 820397662346936340 or message.channel.id == 845587030079045682:
        if message.author == bot.user:
            if message.content.startswith("d") or message.content.startswith("Vo"):
                await asyncio.sleep(5)
                await message.delete()

        elif message.content.startswith('>e'):
            await message.delete()
            if len(message.content.split(' ')) == 1:
                await message.channel.send(codecs.encode(message.attachments[0].url, 'rot_13'))
            else:
                await message.channel.send(codecs.encode(message.content.split(' ')[1], 'rot_13'))

        elif message.content.startswith(">d"):
            await message.delete()
            await message.channel.send("decoded : " + codecs.decode(message.content.split(' ')[1], 'rot_13'))

        elif message.content.startswith(">help"):
            await message.delete()
            await message.channel.send(
                "Voici l'help du bot mon reuf :\n  Pour décoder : `>d`\n  Pour encoder : `>e`\n  Clear le channel : `>clear`\n  Afficher un message permanent : `>say`")

        # Message normal
        else:
            await asyncio.sleep(5)
            await message.delete()

    if message.channel.id == 841405624985190430:
        if message.author != bot.user:
            try:
                await asyncio.sleep(30)
                await message.delete()
            except:
                pass

    if "tg sale bougnoul" in msg:
        if message.author.id == 658989638337429504 or message.author.id == 378234861414252544:
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/667053408636633088/827996156478488646/video0.mov")
        return

    msg = msg.translate(table).rstrip()
    if msg.endswith("quoi"):
        if randint(1, 500) == 355:
            await message.channel.send("feur")
        return

    if msg.endswith("oui"):
        if randint(1, 500) == 355:
            await message.channel.send("stiti")
        return

    if "tg femme" in msg:
        await message.channel.send("Oue ftg stp tu nous casses les couilles")
        return


bot.run(TOKEN)