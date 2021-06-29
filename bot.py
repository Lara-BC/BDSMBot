# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import users
import os
import sys

import logging

from dotenv import load_dotenv

load_dotenv()

#   ##        #######   ######    ######   #### ##    ##  ######
#   ##       ##     ## ##    ##  ##    ##   ##  ###   ## ##    ##
#   ##       ##     ## ##        ##         ##  ####  ## ##
#   ##       ##     ## ##   #### ##   ####  ##  ## ## ## ##   ####
#   ##       ##     ## ##    ##  ##    ##   ##  ##  #### ##    ##
#   ##       ##     ## ##    ##  ##    ##   ##  ##   ### ##    ##
#   ########  #######   ######    ######   #### ##    ##  ######


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler_stdout = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
handler_stdout.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
log.addHandler(handler)
log.addHandler(handler_stdout)

#    ######  ######## ######## ##     ## ########
#   ##    ## ##          ##    ##     ## ##     ##
#   ##       ##          ##    ##     ## ##     ##
#    ######  ######      ##    ##     ## ########
#         ## ##          ##    ##     ## ##
#   ##    ## ##          ##    ##     ## ##
#    ######  ########    ##     #######  ##


description = """An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


@commands.check
def is_me(ctx):
    return ctx.message.author.id == 597562323481395208


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


def letter_to_gagtalk(letter: str):
    was_upper = letter.isupper()
    letter = letter.lower()

    # Normal garble, keep vowels and a few letters the same
    if letter in ("q", "k", "x"):
        letter = "k"
    elif letter in ("w", "y", "j", "l", "r"):
        letter = "a"
    elif letter in ("s", "z"):
        letter = "h"
    elif letter in ("d", "f"):
        letter = "m"
    elif letter in ("p"):
        letter = "f"
    elif letter in ("g"):
        letter = "f"

    letter = letter.upper() if was_upper else letter

    return letter


def message_to_gagtalk(message, level=1):
    return "".join([letter_to_gagtalk(letter) for letter in message])


async def send_gagged_message(
    message: discord.Message
):
    webhooks = await message.channel.webhooks()
    if webhooks:
        webhook = webhooks[0]
    else:
        webhook = await message.channel.create_webhook(
            name="GagTalk", reason="Required to replicate gag talk"
        )

    # Now send it
    await webhook.send(
        content=message_to_gagtalk(message.content),
        username=message.author.display_name,
        avatar_url=message.author.avatar_url,
    )


@bot.command()
@is_me
async def init(ctx):
    log.info(f"INIT: {ctx.author.id}")


@bot.command()
@is_me
async def restart(ctx):
    sys.exit()

@bot.listen()
async def on_message(message):
    ctx = await bot.get_context(message)

    # Only handle these things
    if ctx.command: return

    user = users.get_user(message.author)

    if user.is_gagged:
        log.info(f"MSG [gagged]: {message.author.display_name}")

        await message.delete()
        await send_gagged_message(message)


@bot.command()
async def gag(ctx, *, member: discord.Member):
    log.info(f"GAG: {ctx.author.display_name} gags {member}")

    gag = users.Gag.BALLGAG


    user = users.get_user(member)
    user.bind(gag)

    message = (
        f"{ctx.author.display_name} gags {member.display_name} with a {gag.value}"
    )
    await ctx.send(message)


@bot.command()
async def ungag(ctx, *, member: discord.Member):
    log.info(f"GAG: {ctx.author.display_name} ungags {member}")

    user = users.get_user(member)
    user.unbind(users.BodyPart.MOUTH)

    message = f"{ctx.author.display_name} removes the gag from {member.display_name}"
    await ctx.send(message)


bot.run(os.getenv("TOKEN"))
