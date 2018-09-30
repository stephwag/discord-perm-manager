import discord
from pymongo import MongoClient
from discord.ext.commands import Bot
from discord.ext.commands import CheckFailure
from discord.ext.commands import has_any_role
from discord.ext.commands import has_permissions
from discord.ext.commands import check
import os
import raven
from discord_util import *

rc = raven.Client(os.environ['RAVEN_DSN'], environment=os.environ['RAVEN_ENV'])

BOT_PREFIX = ("?", "!")

dbclient = MongoClient(os.environ['MONGO_IP'], int(os.environ['MONGO_PORT']))
db = dbclient[os.environ['MONGO_DB']]

client = Bot(command_prefix=BOT_PREFIX)
current_roles = []

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

def find_object(objects, name, default=None, error="The object does not exist."):
    for o in objects:
        if o.name.lower() == name.lower() or o.id == name:
            return o

    if default is not None: return default

    raise CheckFailure(error)

def get_channel(name, default=None):
    return find_object(client.get_all_channels(), name, default=default, error="The channel does not exist.")

def get_category(ctx, name, default=None):
    return find_object(ctx.guild.categories, name, default=default, error="The category does not exist.")

def get_role(ctx, name, default=None):
    return find_object(ctx.guild.roles, name, default=default, error="The role does not exist.")

def check_perms(ctx, action, objtype):
    error = "You do not have permission to %s a %s."
    result = db.settings.find_one({ '_id' : ctx.guild.id })

    if result is None:
        raise CheckFailure(error % (action, objtype))
    if result[action] is None:
        raise CheckFailure(error % (action, objtype))
    if result[action][objtype] is None:
        raise CheckFailure(error % (action, objtype))

    u = ctx.guild.get_member(ctx.message.author.id)
    for r in ctx.message.author.roles:
        if r.name in result[action][objtype]: return True

    raise CheckFailure(error % (action, objtype))

@client.group(pass_context=True)
async def channel(ctx):
    if is_bot(ctx): return
    set_raven_ctx(ctx, rc)
    if ctx.invoked_subcommand is None:
        await client.say('Invalid channel command passed...')

@client.group(pass_context=True)
async def role(ctx):
    if is_bot(ctx): return
    set_raven_ctx(ctx)
    if ctx.invoked_subcommand is None:
        await client.say('Invalid role command passed...')

@client.command(pass_context=True)
@has_permissions(manage_guild=True)
async def permcheck(ctx):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        result = db.settings.find_one({ '_id' : ctx.guild.id })
        message = ""

        if result is None:
            await ctx.channel.send("No roles have been set!")
        else:
            if "create" in result:
                if "channel" in result["create"]: message += "Create Channels: " + ", ".join(str(x) for x in result["create"]["channel"]) + "\n"
                if "role" in result["create"]: message += "Create Roles: " + ", ".join(str(x) for x in result["create"]["role"]) + "\n"
            if "edit" in result:
                if "channel" in result["edit"]: message += "Edit Channels: " + ", ".join(str(x) for x in result["edit"]["channel"]) + "\n"
                if "role" in result["edit"]: message += "Edit Roles: " + ", ".join(str(x) for x in result["edit"]["role"]) + "\n"
            if "delete" in result:
                if "channel" in result["delete"]: message += "Delete Channels: " + ", ".join(str(x) for x in result["delete"]["channel"]) + "\n"
                if "role" in result["delete"]: message += "Delete Roles: " + ", ".join(str(x) for x in result["delete"]["role"]) + "\n"
            if "limit_everyone" in result:
                message += "The current role limit is " + str(result['limit_everyone']) + "\n"

        await ctx.channel.send(message)
    except:
        rc.captureException()

@channel.command(pass_context=True)
@has_permissions(manage_guild=True)
async def remove(ctx, action, rolename):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        if action in ["create", "edit", "delete"]:
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$pullAll' : { action + '.channel' : [rolename] } }, upsert=True)
            await ctx.channel.send("Removed role '%s' from being able to %s a channel." % (rolename, action))
        else:
            await ctx.channel.send("Incorrect command.")
    except:
        rc.captureException()

@channel.command(pass_context=True)
@has_permissions(manage_guild=True)
async def add(ctx, action, rolename):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        if action in ["create", "edit", "delete"]:
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$addToSet' : { action + '.channel' : rolename } }, upsert=True)
            await ctx.channel.send("Granted role '%s' permission to be able to %s a channel." % (rolename, action))
        else:
            await ctx.channel.send("Incorrect command.")
    except:
        rc.captureException()

@role.command(pass_context=True)
@has_permissions(manage_guild=True)
async def remove(ctx, action, rolename):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        if action in ["create", "edit", "delete"]:
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$pullAll' : { action + '.role' : [rolename] } }, upsert=True)
            await ctx.channel.send("Removed role '%s' from being able to %s a role." % (rolename, action))
        else:
            await ctx.channel.send("Incorrect command.")
    except:
        rc.captureException()

@role.command(pass_context=True)
@has_permissions(manage_guild=True)
async def add(ctx, action, rolename):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        if action in ["create", "edit", "delete"]:
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$addToSet' : { action + '.role' : rolename } }, upsert=True)
            await ctx.channel.send("Granted role '%s' permission to be able to %s a role." % (rolename, action))
        else:
            await ctx.channel.send("Incorrect command.")
    except:
        rc.captureException()

@role.command(pass_context=True)
@has_permissions(manage_guild=True)
async def limit(ctx, count):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        c = int(count)
        if c > 0:
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$set' : { 'limit_everyone' : c } }, upsert=True)
            await ctx.channel.send("Everyone with no role can only have %i roles now" % (c))
    except (TypeError, ValueError):
        rc.captureException()
        await ctx.channel.send("Sorry, that did not work.")

@role.command(pass_context=True)
@has_permissions(manage_guild=True)
async def unlimited(ctx):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        db.settings.update_one({ '_id' : ctx.guild.id }, { '$unset' : { 'limit_everyone' : "" } }, upsert=True)
        await ctx.channel.send("Everyone can have any number of roles now")
    except:
        rc.captureException()

@role.command(pass_context=True)
@has_permissions(manage_guild=True)
async def minimalist(ctx, mode):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        if mode == "on":
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$set' : { 'minimalist' : True } }, upsert=True)
            await ctx.channel.send("Role hierarchy auto management is now on")
        if mode == "off":
            db.settings.update_one({ '_id' : ctx.guild.id }, { '$set' : { 'minimalist' : False } }, upsert=True)
            await ctx.channel.send("Role hierarchy auto management is now off")
    except:
        rc.captureException()

@channel.command(pass_context=True)
async def create(ctx, name, channel_type="text", category=None):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'create', 'channel')
        c = get_category(ctx, name, ctx.guild.categories[0])
        if channel_type == "text": await ctx.guild.create_text_channel(name, category=c)
        if channel_type == "voice": await ctx.guild.create_voice_channel(name, category=c)
        if channel_type == "category": await ctx.guild.create_category_channel(name, category=c)
        await ctx.channel.send("Channel '%s' is created." % (name))
    except:
        rc.captureException()

@channel.command(pass_context=True)
async def delete(ctx, name, reason=None):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'delete', 'channel')
        channel = get_channel(name)
        await channel.delete(reason=reason)
    except:
        rc.captureException()

@channel.command(pass_context=True)
async def edit(ctx, name, param, value, reason=None):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'edit', 'channel')
        channel = get_channel(name)
        if param == "category": value = get_category(ctx, value)
        await channel.edit(**{ "reason" : reason, param : value })
    except:
        rc.captureException()

@role.command(pass_context=True)
async def create(ctx, name):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'create', 'role')
        client.create_role(name)
    except:
        rc.captureException()

@role.command(pass_context=True)
async def delete(ctx, name, reason=None):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'delete', 'role')
        role = get_role(ctx, name)
        role.delete(reason=reason)
    except:
        rc.captureException()

@role.command(pass_context=True)
async def edit(ctx, name, param, value, reason=None):
    try:
        if is_bot(ctx): return
        set_raven_ctx(ctx, rc)
        check_perms(ctx, 'edit', 'role')
        role = get_role(ctx, name)
        if param == "permissions": value = discord.Permissions(value)
        if param == "color" or param == "colour": value = discord.Color(int(value, 16))
        await role.edit(**{ "reason" : reason, param : value })
    except:
        rc.captureException()

async def on_member_update(before, after):
    try:
        if after.bot: return
        set_raven_user(after, rc)
        result = db.settings.find_one({ '_id' : after.guild.id })
        if result is not None:
            if 'limit_everyone' in result and len(before.roles) < len(after.roles):
                thelimit = int(result['limit_everyone'])
                # Because the @everyone role is included, which can't be deleted
                if (len(after.roles) - 1) > thelimit:
                    # Now have to find the role that was added and remove it
                    ids = {}
                    for r in before.roles:
                        ids[r.id] = r
                    for r in after.roles:
                        if r.id not in ids:
                            await after.remove_roles(r, reason="Reached the role limit, which is " + str(thelimit) + " for everyone.")

            if "minimalist" in result and len(before.roles) < len(after.roles):
                if result["minimalist"]:
                    delete_roles = after.roles[1:]
                    for r in delete_roles:
                        await after.remove_roles(r, reason="Role hierarchy management is on.")
    except:
        rc.captureException()

client.add_listener(on_member_update, 'on_member_update')
client.add_cog(DiscordBotsOrgAPI(client))
client.run(os.environ['DISCORD_TOKEN'])
