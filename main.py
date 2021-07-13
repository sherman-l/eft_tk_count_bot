from kill_history import Kill_history
from kill_record import Kill_record
from dotenv import load_dotenv
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

### Keys ###
player_kill_stats = "player_kill_stats"
kill_count = "kill_count"
kill_log = "kill_log"
user_name = "user_name"


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
      
  
client.run(os.getenv('TOKEN'))
