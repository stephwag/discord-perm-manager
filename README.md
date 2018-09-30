# Discord Perm Manager
A Discord bot that allows you to have finer control over granting role permissions on your guild/server.

## What does it do?

What if you could break down the `MANAGE_CHANNELS` permission into these?

`CREATE_CHANNELS`

`EDIT_CHANNELS`

`DELETE_CHANNELS`

That is what this bot does!

This bot can also

* Remove role(s) when a higher role is given. 
* Limit the number of roles a user can assign to themselves.

## Example

Let's say you have a friend with the role `verychatty`. You want to let them create their own channels so they can talk there instead.

But wait...Discord only has a `MANAGE_CHANNELS` permission for updating channels, meaning they also get to edit and delete them, too.

Instead of doing that, you decide to [add this bot to your server](https://discordapp.com/api/oauth2/authorize?client_id=468191417194381322&permissions=268435472&redirect_uri=https%3A%2F%2F206.81.4.56&scope=bot), grant the bot the `MANAGE_CHANNELS` permission, then run this command to allow your friend to *only* create channels.

`!channel add create verychatty`

Now your friend can run this command to create channels

`!channel create meme-shack "lookin' for the meme getaway"`

Now your friend can post all their dank memes in the `meme-shack` channel. However, they won't be able to delete or edit `meme-shack`. You can change that by running `!channel add edit verychatty` or `!channel add delete verychatty`.

If your friend starts spamming the server with a bunch of meme channels, you can remove their role from the "create channel" list by running this command.

`!channel remove create verychatty`

If you're unsure about what roles are configured with the bot, just run `!permcheck`.

## Notes

This bot only supports `MANAGE_CHANNELS` and `MANAGE_ROLES` (only roles themselves, not applying roles to a user). This might change in the future.

It is **strongly recommended** that you only give this bot `MANAGE_CHANNELS` and `MANAGE_ROLES` permission, as it doesn't need to be an admin.

## Support or Contact

Support server: [https://discord.gg/PAATvBs](https://discord.gg/PAATvBs)

## Commands

### Channels

| Command | Description | Usage |
|----------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **!channel create** | Creates a channel | `!channel create [name] (optional reason)` |
| **!channel edit** | Edits a channel by setting a field to a specific value. See **Channel Fields** for details. | `!channel edit [name] [field] [value] (optional reason)` |
| **!channel delete** | Deletes a channel | `!channel delete [name] (optional reason)` |
| **!channel add create** | Allow a role to create channels. | `!channel add create [role]` |
| **!channel add edit** | Allow a role to edit channels. | `!channel add edit [role]` |
| **!channel add delete** | Allow a role to delete channels. | `!channel add delete [role]` |
| **!channel remove create** | Disallow a role from creating channels. | `!channel remove create [role]` |
| **!channel remove edit** | Disallow a role from editing channels. | `!channel remove edit [role]` |
| **!channel remove delete** | Disallow a role from deleting channels. | `!channel remove delete [role]` |

### Roles

| Command | Description | Usage |
|----------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **!role create** | Creates a role | `!role create [name] (optional reason)` |
| **!role edit** | Edits a role by setting a field to a specific value. See **Role Fields** for details. | `!role edit [name] [field] [value] (optional reason)` |
| **!role delete** | Deletes a role | `!role delete [name] (optional reason)` |
| **!role add create** | Allow a role to create role. | `!role add create [role]` |
| **!role add edit** | Allow a role to edit role. | `!role add edit [role]` |
| **!role add delete** | Allow a role to delete role. | `!role add delete [role]` |
| **!role remove create** | Disallow a role from creating role. | `!role remove create [role]` |
| **!role remove edit** | Disallow a role from editing role. | `!role remove edit [role]` |
| **!role remove delete** | Disallow a role from deleting role. | `!role remove delete [role]` |
| **!role limit** | Limit the number of roles everyone can assign to themselves (including mods) | `!role limit [number]` |
| **!role unlimited** | Allow any number of roles everyone can assign to themselves (including mods) | `!role unlimited` |
| **!role minimalist on** | When a higher role is given to a user, all roles below that role are deleted | `!role minimalist on` |
| **!role minimalist off** | Turns off the above command | `!role minimalist off` |

### Misc

| Command | Description | Usage |
|----------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **!permcheck** | List all roles and their custom permissions that are currently configured with this bot. | `!permcheck` |

## Fields

### Channel Fields

| Field | Type | Description | Example |
|------------------|---------|------------------------------------------------------------------------------|--------------------------------------------------|
| **name** | string | Sets the channel name |  |
| **topic** | string | Sets the channel topic |  |
| **position** | integer | Sets the channel position within its category. |  |
| **nsfw** | boolean | Sets the channel NSFW flag. | `!channel edit mychannel nsfw True` |
| **sync_permissions** | boolean | Whether to sync permissions with the channel’s new or pre-existing category. |  |
| **category** | string | The new category for this channel. Can be **None** to remove the category. | `!channel edit mychannel category "text channels"` |

### Role Fields

| Field | Type | Description | Example |
|-------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| **name** | string | Sets the role name |  |
| **permissions** | integer | Sets the permission for the role. [You can use this permission calculator](https://discordapi.com/permissions.html) to figure out the number to use. | `!role edit myrole permissions 402653216` |
| **color** (or **colour**) | hex | Sets the role color.  | `!role edit myrole color 314b74` |
| **hoist** | boolean | Indicates if the role should be shown separately in the member list. |  |
| **mentionable** | boolean | Indicates if the role should be mentionable by others. |  |
| **position** | string | The new role’s position. This must be below your top role’s position or it will fail. |  |
