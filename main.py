# all imports that need
import discord
import os
import json
from discord.ext import commands
# bot token 
TOKEN = "Paste here your bot TOKEN"

client = commands.Bot(command_prefix=".", case_insensitive=True)
client.remove_command('help')

# Gimme credits nub

@client.event
async def on_ready():
  print('Tutorial Bot is ready!')
  await client.change_presence(activity=discord.Game('Subscribe!'))

@client.event
async def on_command_error(ctx, error):
  embed = discord.Embed(
  title='',
  color=discord.Color.red())
  if isinstance(error, commands.CommandNotFound):
    pass
  if isinstance(error, commands.MissingPermissions):
    embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
    await ctx.send(embed=embed)
  else:
    embed.add_field(name=f':x: Terminal Error', value=f"{error}")
    await ctx.send(embed=embed)
    raise error

@client.command()
async def ping(ctx):
  await ctx.send(f'My ping is `{round(client.latency * 1000)}ms`!')

@client.command()
async def help(ctx):
  with open("help.json") as f:
    data = json.load(f)
  embed = discord.Embed(title="Tutorial | Help Panel", description="Lists all of my commands!",
  colour=0x52b788)
  embed.set_footer(text=f"Requested by {ctx.author.name} | Tutorial", icon_url=ctx.author.avatar_url)
  data = json.load(open("help.json"))
  for key, value in data.items():
    embed.add_field(name=key, value=value, inline=False)
  await ctx.reply(embed=embed)

@client.command(aliases=['r'])
async def report(ctx, member:discord.Member, *, report=None):
  report_channel = discord.utils.get(ctx.guild.channels, name = 'reports')
  if member is None:
    return await ctx.send("Please include a user you want to report.")
  if report is None:
    return await ctx.send("Please include information about the report.")
  else:
    embed = discord.Embed(title="Report", description=f"{ctx.author.mention} has reported {member} | Tutorial", colour=0x52b788)
    embed.set_thumbnail(url="")
    embed.add_field(name="More Info:", value=f"{report}")
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"React with the ✅ if the situation has been dealt with. | Tutorial")
    report_message = await report_channel.send(embed=embed)
    await report_message.add_reaction('✅')
    await ctx.send(f"{ctx.author.mention} Your report has been sent to the staff team!")

    try:
      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅"]

      reaction, user = await client.wait_for("reaction_add", timeout=604800, check=check)

      if str(reaction.emoji) == "✅":
        await ctx.author.send("Your report has been looked into and dealt with. Thank you for reporting!")

    except Exception as e:
      print(e)

@client.command()
async def suggest(ctx, *, suggestion):
  await ctx.channel.purge(limit=1)
  channel = client.get_channel(836295455658868736)

  suggestEmbed = discord.Embed(colour=0x52b788)
  suggestEmbed.set_author(name=f'Suggested by {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
  suggestEmbed.add_field(name='New Suggestion!', value=f'{suggestion}')

  message = await channel.send(embed=suggestEmbed)

  await message.add_reaction('✅')
  await message.add_reaction('❌')

client.run('TOKEN')