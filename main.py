from kill_history import KillHistory
from kill_record import KillRecord
from dotenv import load_dotenv
from queue import PriorityQueue
import os
import json
import discord
import db_read_write as db
import language_service as ls
import strings_keys as skey

### Set all intents so that discord can have access to the member list ###
intents = discord.Intents.all()
client = discord.Client(intents = intents)
db_name = "kill_db.json"
language_settings = {}
load_dotenv()

### Keys ###
player_kill_stats = "player_kill_stats"
kill_count = 'kill_count'
kill_log = 'kill_log'
killer_id = 'killer_id'
killed_id = 'killed_id'
date_of_kill = 'date_of_kill'
user_name = 'user_name'
rankings = 'rankings'
language = 'language'
server_id = 'server_id'

### Settings ###
default_log_count = '10'
reaction_timeout = 30.0

# Fetch user object from user_id string
async def get_user_obj(user_id):
  user = await client.fetch_user(int(user_id))
  return user
  
# Fetch user name from user_id string
async def get_user_name(user_id):
  user = await client.fetch_user(int(user_id))
  return user.name

# Adds syntax to string necessary to mention a user within discord
def mention_user(user_id):
  return "<@!" + user_id + ">"

# Creates an empty record for a server
def create_server_record(json_obj, server):
  json_obj[server] = {}
  json_obj[server][server_id] = server
  json_obj[server][player_kill_stats] = {}
  json_obj[server][kill_log] = []
  json_obj[server][language] = 'en'
  return json_obj  

# Embeds rank stats for all users stored within the rank priority queue
def embed_rank_stats(rank_pqueue, server_json_obj):
  server_language = language_settings.get(server_json_obj[server_id])
  embed = discord.Embed(
    title = ls.get_string(server_language, skey.tk_rankings),
    colour = discord.Colour.from_rgb(255,255,0)    
  )
  rank = 1
  while not rank_pqueue.empty():
    next_record = rank_pqueue.get()
    user_stats = server_json_obj[player_kill_stats][next_record[1]]
    embed.add_field(
      name = "#" + str(rank),
      value = user_stats[user_name],
      inline = True
    )
    # Empty field for formatting
    embed.add_field(
      name = '\u200b',
      value = '\u200b',
      inline = True      
    )
    embed.add_field(
      name = ls.get_string(server_language, skey.embed_kill_count),
      value = str(user_stats[kill_count]),
      inline = True
    )
    embed.add_field(
      name = '\u200b',
      value = '\u200b',
      inline = False      
    )
    rank = rank + 1
    
  # Remove extra space at the end 
  embed.remove_field(len(embed.fields) - 1)
  return embed

async def handle_rank(message):
  server = str(message.guild.id)
  server_language = language_settings.get(server)
  json_obj = db.load_db_json(db_name)
  server_json_obj = json_obj[server]
  rank_pqueue = PriorityQueue()
  if server in json_obj:
    rank = 1
    return_string = ""
    for player_id in server_json_obj[player_kill_stats]:
      entry = server_json_obj[player_kill_stats][player_id]
      rank_pqueue.put((-entry[kill_count], player_id))
    embed = embed_rank_stats(rank_pqueue, server_json_obj)
    await message.channel.send(embed = embed)      
  else:
    await message.channel.send(ls.get_string(server_language, skey.no_statistics_server))
    return

async def handle_log(message):
  server = str(message.guild.id)
  server_language = language_settings.get(server)
  params = message.content.split()
  # Set default log entries to print to 10 when user does not specify a number
  if len(params) < 2:
    params.append(default_log_count)
  
  # Sends error message if 1st param entered is not a number
  if not params[1].isdigit():
    await message.channel.send(ls.get_string(server_language, skey.log_invalid_params))
    return
  json_obj = db.load_db_json(db_name)
  log_json_obj = json_obj[server][kill_log]
  index_ceiling = int(params[1])
  count = 0
  return_string = ""
  while count < index_ceiling and count < len(log_json_obj):
    index = len(log_json_obj) - (count + 1)
    return_string = return_string + ls.get_string(server_language, skey.log_string).format(await get_user_name(log_json_obj[index][killer_id]), await get_user_name(log_json_obj[index][killed_id]), log_json_obj[index][date_of_kill]) + '\n'
    count += 1
  await message.channel.send(return_string)

# Sets reactions onto an embed message such that the person requesting command can flip through
# different pages of data using the reaction controls  
async def add_reaction_controls_to_embed(message, footer_message, pages):
  server_language = language_settings.get(str(message.guild.id))
  pages[0].set_footer(text=footer_message.format(1, str(len(pages))))
  sent_message = await message.channel.send(embed = pages[0])
  await sent_message.add_reaction('⏮')
  await sent_message.add_reaction('◀')
  await sent_message.add_reaction('▶')
  await sent_message.add_reaction('⏭')
  
  # Checks whether user who reacted is the same as the user who requested command
  def check(reaction, user):
    return user == message.author
      
  i = 0
  reaction = None
  show_page = pages[i]
  while True:
    if str(reaction) == '⏮':
      i = 0
      show_page = pages[i]
      show_page.set_footer(text=ls.get_string(server_language, skey.stats_embed_footer).format(i + 1, str(len(pages))))
      await sent_message.edit(embed = show_page)
    elif str(reaction) == '◀':
      if i > 0:
        i -= 1
        show_page = pages[i]
        show_page.set_footer(text=ls.get_string(server_language, skey.stats_embed_footer).format(i + 1, str(len(pages))))
        await sent_message.edit(embed = show_page)
    elif str(reaction) == '▶':
      if i < len(pages) - 1:
        i += 1
        show_page = pages[i]
        show_page.set_footer(text=ls.get_string(server_language, skey.stats_embed_footer).format(i + 1, str(len(pages))))
        await sent_message.edit(embed = show_page)
    elif str(reaction) == '⏭':
      i = len(pages) - 1
      show_page = pages[i]
      show_page.set_footer(text=ls.get_string(server_language, skey.stats_embed_footer).format(i + 1, str(len(pages))))
      await sent_message.edit(embed = show_page)
        
    try:
      reaction, user = await client.wait_for('reaction_add', timeout = reaction_timeout, check = check)
      await sent_message.remove_reaction(reaction, user)
    except:
      break
  await sent_message.clear_reactions()

async def handle_stats(message, user = None):
  server = str(message.guild.id)
  server_obj = client.get_guild(message.guild.id)
  server_language = language_settings.get(server)
  json_obj = db.load_db_json(db_name)
  
  # If user or server does not exist in db, print error message
  if server in json_obj:
    if user != None:
      user_id = str(user.id)
      if user_id in json_obj[server][player_kill_stats]:
        await message.channel.send(embed = embed_stats(message, json_obj[server], user, json_obj[server][language]))
      else:
        await message.channel.send(ls.get_string(server_language, skey.no_statistics_user).format(mention_user(user_id)))
    else:
      pages = []
      for member in server_obj.members:
        if str(member.id) in json_obj[server][player_kill_stats]:
          stats_embed = embed_stats(message, json_obj[server], member)
          pages.append(stats_embed)
      await add_reaction_controls_to_embed(message, ls.get_string(server_language, skey.stats_embed_footer), pages)

  else: 
    await message.channel.send(ls.get_string(server_language, skey.no_statistics_server))
  
# Embeds the result of $stats command into a discord Embed
def embed_stats(message, server_json_obj, user):
  server = str(message.guild.id)
  server_language = language_settings.get(server)
  user_stats = discord.Embed(
    title = ls.get_string(server_language, skey.embed_stats_title).format(user.name),
    colour = discord.Colour.from_rgb(255,0,0)
  )
  user_stats.set_thumbnail(url = user.avatar_url)
  user_stats.add_field(name = ls.get_string(server_language, skey.embed_kill_count), value = server_json_obj[player_kill_stats][str(user.id)][kill_count])
  return user_stats

async def handle_tk(message):
  server = str(message.guild.id)
  server_language = language_settings.get(server)
  killer = message.mentions[0]
  killed = message.mentions[1]
  tk_history = KillHistory(killer.id, killed.id, message.created_at)
  json_obj = db.load_db_json(db_name) 
  
  add_tk_to_obj(json_obj, server, killer)
  kill_log_entry = tk_history.to_json()
  json_obj[server][kill_log].append(kill_log_entry)
  db.write_db_json(db_name, json_obj)
  await message.channel.send(ls.get_string(server_language, skey.tk_log_entry_success).format(mention_user(str(killer.id)), mention_user(str(killed.id))))

# Adds server and user entry into db if it does not exist, adds 1 to the kill count of the user otherwise
def add_tk_to_obj(json_obj, server, killer):
  if server not in json_obj:
    json_obj = create_server_record(json_obj, server)
    
  if str(killer.id) in json_obj[server][player_kill_stats]:
    json_obj[server][player_kill_stats][str(killer.id)][kill_count] += 1
  else:
    player_entry = KillRecord(killer.id, killer.name, 1)
    json_obj[server][player_kill_stats][str(killer.id)] = player_entry.to_json()

async def handle_lang(message):
  params = message.content.split()
  server = str(message.guild.id)
  server_language = language_settings.get(server)
  json_obj = db.load_db_json(db_name)
  if len(params) < 2:
    await message.channel.send(ls.get_string(server_language, skey.lang_insufficient_parameters))
    return
  
  if server not in json_obj:
    create_server_record(json_obj, server)
    
  if params[1] == 'jp':
    json_obj[server][language] = 'jp'
    language_settings[server] = 'jp'
    await message.channel.send(ls.get_string(language_settings[server], skey.lang_change_success))
  elif params[1] == 'en':
    json_obj[server][language] = 'en'
    language_settings[server] = 'en'
    await message.channel.send(ls.get_string(language_settings[server], skey.lang_change_success))
  else:
    await message.channel.send(ls.get_string(server_language, skey.lang_unrecognized_language))
    return
  db.write_db_json(db_name, json_obj)

@client.event
async def on_ready():
    json_obj = db.load_db_json(db_name)
    for server in json_obj:
      language_settings[server] = json_obj[server][language]
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$tk'):
    if len(message.mentions) != 2:
      await message.channel.send(ls.get_string(language_settings.get(str(message.guild.id)), skey.tk_invalid_params))
    else:
      await handle_tk(message)
      return
    
  if message.content.startswith('$stats'):
    # Loads stats for a single user that has been mentioned
    if len(message.mentions) == 1:
      await handle_stats(message, message.mentions[0])
    # Loads stats all users that have a kill stats if $stats is called with no params
    elif len(message.content.split()) == 1:
      await handle_stats(message)    
    else:
      await message.channel.send(ls.get_string(language_settings.get(str(message.guild.id)), skey.stats_invalid_params))
      return
  
  if message.content.startswith('$log'):
    await handle_log(message)   
    return
  
  if message.content.startswith('$rank'):
    await handle_rank(message)
    return
  
  if message.content.startswith('$lang'):
    await handle_lang(message)
    return 
client.run(os.getenv('TOKEN'))
