from kill_history import Kill_history
from kill_record import Kill_record
import os
import json
import discord

client = discord.Client()

def mention_user(user_id):
  return "<@!" + user_id + ">"

def load_db_json():
  kill_db = open("kill_db.json", "r")
  json_obj = json.load(kill_db)
  kill_db.close()
  return json_obj
  
def write_db_json(json_obj):
  kill_db = open("kill_db.json", "w")
  json.dump(json_obj, kill_db, indent=4)
  kill_db.close()

async def handle_tk(message):
  killer = message.mentions[0]
  killed = message.mentions[1]
  tk_history = Kill_history(killer.id, killed.id, message.created_at)
  json_obj = load_db_json()
        
  if tk_history.killer_id in json_obj["player_kill_stats"]:
    json_obj["player_kill_stats"][tk_history.killer_id]["kill_count"] += 1
  else:
    json_obj["player_kill_stats"][tk_history.killer_id] = {}
    json_obj["player_kill_stats"][tk_history.killer_id]["kill_count"] = 1
    json_obj["player_kill_stats"][tk_history.killer_id]["user_name"] = killer.name
    await message.channel.send(mention_user(tk_history.killer_id) + " team killing " + mention_user(tk_history.killed_id) + " log entered!")

  kill_log_entry = json.loads(tk_history.to_json_string())
  json_obj["kill_log"].append(kill_log_entry)
  print(json_obj)
  write_db_json(json_obj)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$tk'):
    print(message.mentions)
    if len(message.mentions) != 2:
      await message.channel.send('Invalid number of params! Appropriate use: ```\'$tk @killer @killed\'```')
      return
    await handle_tk(message)
        
client.run(os.getenv('TOKEN'))
