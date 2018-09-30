import discord
from discord.ext.commands import CheckFailure
import dbl
import raven
import os
import asyncio

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ['STATS_TOKEN']
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            try:
                await self.dblpy.post_server_count()
            except Exception as e:
                rc.captureException()
            await asyncio.sleep(3600)

def set_raven_ctx(ctx, rc):
    c = {
        'id' : ctx.message.author.id,
        'user_name' : ctx.message.author.name,
        'is_bot': ctx.message.author.bot,
        'user_discriminator' : ctx.message.author.discriminator,
        'created_at': ctx.message.author.created_at,
        'message_id' : ctx.message.id,
        'message_content' : ctx.message.content
    }

    if ctx.guild is not None:
        c['guild_id'] = ctx.guild.id
        c['guild_name'] = ctx.guild.name

    rc.user_context(c)

def is_bot(ctx):
    return ctx.author.bot

