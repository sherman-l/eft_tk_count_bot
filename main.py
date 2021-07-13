from kill_history import Kill_history
from kill_record import Kill_record
from dotenv import load_dotenv
from queue import PriorityQueue
import os
import json
import discord

client = discord.Client()
db_name = "kill_db.json"
load_dotenv()

### Error Strings ###
tk_invalid_params = 'Invalid number of params! \nAppropriate usage: ```$tk @killer @killed```'
stats_invalid_params = 'Incorrect usage! ```$stats @user```'

### General Message Strings ###
no_statistics_user = 'No stats available for {}'
no_statistics_server = 'No stats available for server'
kill_stats = 'User: {} \nTeam Kills: {}'
log_string = 'Team Killer: {} \t Victim: {} \t Date: {}'
ranking_row = 'Rank: {} \tName: {} \tKill Count: {}'

### Keys ###
player_kill_stats = "player_kill_stats"
kill_count = "kill_count"
kill_log = "kill_log"
killer_id = "killer_id"
killed_id = "killed_id"
date_of_kill = "date_of_kill"
user_name = "user_name"


async def get_user_name(user_id):
  print(user_id)
  user = await client.fetch_user(int(user_id))
  print(user)
  return user.name

def mention_user(user_id):
  return "<@!" + user_id + ">"

def load_db_json():
  if not os.path.isfile(db_name):
    with open(db_name, "w") as db_file:
      db_file.write(json.dumps({}))
  kill_db = open(db_name, "r")
  json_obj = json.load(kill_db)
  kill_db.close()
  return json_obj
  
def write_db_json(json_obj):
  kill_db = open(db_name, "w")
  json.dump(json_obj, kill_db, indent=4)
  kill_db.close()

async def handle_rank(message):
  server = str(message.guild.id)
  json_obj = load_db_json()
  server_json_obj = json_obj[server]
  rank_pqueue = PriorityQueue()
  if server in json_obj:
    rank = 1
    return_string = ""
    for player_id in server_json_obj[player_kill_stats]:
      entry = server_json_obj[player_kill_stats][player_id]
      rank_pqueue.put((entry[kill_count], entry))
    while not rank_pqueue.empty():
      next_record = rank_pqueue.get()
      print(next_record[1][kill_count])
      return_string = return_string + ranking_row.format(str(rank), next_record[1][user_name], str(next_record[1][kill_count])) + "\n"
      rank += 1
    await message.channel.send(return_string)      
  else:
    await message.channel.send(no_statistics_server)
    return

async def handle_log(message):
  server = str(message.guild.id)
  params = message.content.split()
  if not params[1].isdigit():
    return
  json_obj = load_db_json()
  log_json_obj = json_obj[server][kill_log]
  index_ceiling = int(params[1])
  count = 0
  return_string = ""
  while count < index_ceiling and count < len(log_json_obj):
    index = len(log_json_obj) - (count + 1)
    return_string = return_string + log_string.format(await get_user_name(log_json_obj[index][killer_id]), await get_user_name(log_json_obj[index][killed_id]), log_json_obj[index][date_of_kill]) + '\n'
    count += 1
  await message.channel.send(return_string)    
  

async def handle_stats(message):
  server = str(message.guild.id)
  user = str(message.mentions[0].id)
  json_obj = load_db_json()
  if server in json_obj:
    if user in json_obj[server][player_kill_stats]:
      result_message = kill_stats.format(mention_user(user), json_obj[server][player_kill_stats][user][kill_count])
      await message.channel.send(result_message)
    else:
      await message.channel.send(no_statistics_user.format(mention_user(user)))
  else: 
    await message.channel.send(no_statistics_server)

async def handle_tk(message):
  server = str(message.guild.id)
  killer = message.mentions[0]
  killed = message.mentions[1]
  tk_history = Kill_history(killer.id, killed.id, message.created_at)
  json_obj = load_db_json()  
  
  if server not in json_obj:
    json_obj[server] = {}
    json_obj[server][player_kill_stats] = {}
    json_obj[server][kill_log] = []
    
  if tk_history.killer_id in json_obj[server][player_kill_stats]:
    json_obj[server][player_kill_stats][tk_history.killer_id][kill_count] += 1
  else:
    json_obj[server][player_kill_stats][tk_history.killer_id] = {}
    json_obj[server][player_kill_stats][tk_history.killer_id][kill_count] = 1
    json_obj[server][player_kill_stats][tk_history.killer_id][user_name] = killer.name
    await message.channel.send(mention_user(tk_history.killer_id) + " team killing " + mention_user(tk_history.killed_id) + " log entered!")

  kill_log_entry = json.loads(tk_history.to_json_string())
  json_obj[server][kill_log].append(kill_log_entry)
  write_db_json(json_obj)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$tk'):
    if len(message.mentions) != 2:
      await message.channel.send(tk_invalid_params)
      return
    await handle_tk(message)
    
  if message.content.startswith('$stats'):
    if len(message.mentions) != 1:
      await message.channel.send(stats_invalid_params)
      return
    await handle_stats(message)
  
  if message.content.startswith('$log'):
    await handle_log(message)   
  
  if message.content.startswith('$rank'):
    await handle_rank(message)   
  
client.run(os.getenv('TOKEN'))
