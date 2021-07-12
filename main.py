from replit import db
from kill_history import Kill_history
from kill_record import Kill_record
import os
import json
import discord

client = discord.Client()

def mention_user(user_id):
  return "<@!" + str(user_id) + ">"

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
        killer = message.mentions[0]
        killed = message.mentions[1]
        this_kill_history = Kill_history(killer.id, killed.id, message.created_at)
        kill_db = open("kill_db.json", "r")
        json_obj = json.load(kill_db)
        kill_db.close()
        if killer.id in json_obj["player_kill_stats"].keys():
          json_obj["player_kill_stats"][killer.id]["kill_count"] += 1
        else:
          json_obj["player_kill_stats"][killer.id] = {}
          json_obj["player_kill_stats"][killer.id]["kill_count"] = 1
          json_obj["player_kill_stats"][killer.id]["user_name"] = killer.name
        await message.channel.send("<@!" + str(killer.id) + "> has killed <@!" + str(killed.id) + ">")
        print(json_obj)

        
client.run(os.getenv('TOKEN'))
