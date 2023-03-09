import os
import json

from hook.discordparser import *

from utils.embedlogger import EmbedLogger

PREFIX = os.getenv("DEFAULT_DISCORD_PREFIX")
BOTNAME = os.getenv("DEFAULT_BOTNAME")

if __name__ == "__main__":
    # Logger being passed/used to all functions
    logger = EmbedLogger(name=BOTNAME, verbose=True)
    
    bot = commands.Bot(command_prefix=PREFIX)
    
    @bot.event
    async def on_ready():
        logger.info("SpeculBot up and running!")

    @bot.command(name='add', help=f"Add a bot to SpeculBot")
    async def add_bot(ctx, *args):
        await ctx.send(f"")

    @bot.command(name='remove', help="Remove a bot from SpeculBot")
    async def remove_bot(ctx, *args):
        await ctx.send(f"")
    
    @bot.command(name='list', help="List all bots in SpeculBot")
    async def list_bots(ctx, *args):
        await ctx.send(f"")

    token_path = os.getenv("BOT_TOKEN_FILE")
    if token_path is None: quit()

    # Read token from a Json file (manually added)
    with open(token_path, 'r') as file:
        TOKEN = json.load(file)["TOKEN"]

    try:
        # Start SpeculBot
        bot.run(TOKEN)

    except KeyboardInterrupt:
        quit()