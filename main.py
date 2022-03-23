import discord
import os
from replit import db
import requests
import keep_alive
import json

url1 = "https://api.mozambiquehe.re/bridge?version=5&platform=PC&player="
url2 = "&auth="
name_api = "https://api.mozambiquehe.re/nametouid?player="
name_api_2 = "&platform=PC&auth="
player_name = "zWabiSabi"
history_api_1 = "https://api.mozambiquehe.re/games?auth="
history_api_2 = "&uid="
trgg_url_1 = "https://public-api.tracker.gg/v2/apex/standard/profile/origin/"
trgg_key =  os.environ["trgg_key"]
api_key = os.environ["api_key"]
token = os.environ["token"]
pred_url = "https://api.mozambiquehe.re/predator?auth="
r = requests.get(url1 + player_name + url2 + api_key)
data = json.loads(r.content)

client = discord.Client()
print("Starting...")

@client.event
async def on_ready():
    print("SU Apex Running as {0.user}".format(client))
    g = client.guilds
    print("In servers: ")
    for gld in g:
      print(gld)
      for channel in gld.text_channels:
        print(channel)

@client.event
async def on_message(message):
  if message.author == client.user:
        return
  if message.content.startswith('!stats'):
    player_name = message.content.split('!stats ')[1]
    r = requests.get(url1 + player_name + url2 + api_key)
    uuid_data = requests.get(name_api + player_name + name_api_2 + api_key)
    data = json.loads(r.content)
    uuid = json.loads(uuid_data.content)["uid"]
    history_data = requests.get(history_api_1 + api_key + history_api_2 + uuid)
    #history =json.loads(history_data)
    print(history_data)
    print(history_api_1 + api_key + history_api_2 + uuid)
    #print(uuid)
    
    selected_hero = data["legends"]["selected"]["LegendName"]
    try:
      hero_stats = data['legends']["all"][selected_hero]
    except KeyError:
      print("oops")
    #print(selected_hero)
    #print(hero_stats)
    #Get Trackernet Stats
    #TODO
    #trgg_data = json.loads(r_trgg.content)
    #print(trgg_data)
    #------------------------------------------
    embed=discord.Embed(title=("Stats for " + player_name), description="Stats", color=0x00fe15)
    embed.set_thumbnail(url=data["global"]["rank"]["rankImg"])
    embed.add_field(name="Level", value=data["global"]["level"], inline=True)
    embed.add_field(name="Rank", value=data["global"]["rank"]["rankName"] + " " + str(data["global"]["rank"]["rankDiv"]), inline=True)
    embed.add_field(name="RP", value=data["global"]["rank"]["rankScore"], inline=True)
    embed.add_field(name="Legend", value=selected_hero, inline=False)
    try:
      for value in hero_stats["data"]:
        embed.add_field(name=value["name"], value=value["value"], inline=False)
    except KeyError:
      embed.add_field(name="Stats ", value= "NaN")
    #-------------------------------------------
    
    await message.channel.send(embed=embed)
  if message.content.startswith('!pred'):
    pred_data = requests.get(pred_url + api_key)
    pred = json.loads(pred_data.content)["RP"]["PC"]
    embed=discord.Embed(title="Min RP for Pred", description="Stats", color=0x00fe15)
    embed.set_thumbnail(url="https://preview.redd.it/nuy3x9cw1v831.png?auto=webp&s=1361fbae9752a6b7bc55fb05e3826728b4a1e4e3")
    embed.add_field(name="Predator RP Value:", value=pred["val"], inline=True)
    await message.channel.send(embed=embed)

if __name__ == "__main__":
  keep_alive.keep_alive()
  client.run(token)