# various imports required; command for bot commands, discord for the bot, etc
import json
from unittest import result
from discord.gateway import DiscordClientWebSocketResponse
import requests
import discord
from discord.ext import commands
from urllib import response

# need this in order for commands to work because discord is very epic!
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "$", intents = intents)

# tokens for discord and riot 
discordToken = 'use your token'
ritoToken = 'use your token'

# gets rid of spaces between words so determiner and inputting usernames can work
def formatter(nameWithSpace):
    result =  result = " ".join(str(i) for i in nameWithSpace)
    return result

""" 
function to get profile; name of the user and the region its from
currently only support NA, EUW, and KR
if the region matches one of the 3 then it will request a http call and return
the value of the http link and convert it to json format where I am able to then
set the name, level to a variable and use the profile icon i got from the json format
to find the correct image
"""
def profile(region, name):
    if region == "na":
        ritoAPI = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + ritoToken
    if region == "euw":
        ritoAPI = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + ritoToken
    if region == "kr":
        ritoAPI = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + ritoToken
    response = requests.get(ritoAPI)
    jsonSummonerData = response.json()
    summonerName = jsonSummonerData["name"]
    summonerID = jsonSummonerData['id']
    summonerLevel = "Level: " + str(jsonSummonerData["summonerLevel"])
    summonerIcon = "https://ddragon.leagueoflegends.com/cdn/12.19.1/img/profileicon/" + str(jsonSummonerData["profileIconId"]) + ".png"
    return (summonerName, summonerLevel, summonerIcon, summonerID)

def rank(region, summonerID):
    if region == "na":
        ritoAPI = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerID + "?api_key=" + ritoToken
    if region == "euw":
        ritoAPI = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerID + "?api_key=" + ritoToken
    if region == "kr":
        ritoAPI = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerID + "?api_key=" + ritoToken
    response = requests.get(ritoAPI)
    jsonSummonerData = response.json()
    results = {0:"queueType", 1:"tier", 2:"rank", 3:"leaguePoints", 4:"wins", 5:"losses"}
    printList = []
    #range of 2 because only printing solo and flex results; nested loop range of 6
    #for the queue type, tier, rank, etc then append it to empty array to use
    #required because the data is an array with 2 elements and each element has a dict
    # of the results; 2*6 = 12
    for i in range(2):
        for j in range(6):
            summonerList.append(jsonSummonerData[i][results[j]])
    return summonerList
    

"""
called profile function with 3 different regions for the first argument and then the name
and get 3 values in return and I set user equal to that
"""
"""
I create an embed with the title being the first return value of user,
description being the second return value, and thumbnail being the third return value.
this correlates to name, level and icon where name = 0, name = 1, name = 2
"""    
@bot.command()
async def na(ctx, *nameWithSpace):
    name = formatter(nameWithSpace)
    user = profile("na", name)
    userRank = rank("na", user[3])
    embed = discord.Embed(title = user[0], description = user[1], color = 0xA5240C)
    embed.set_thumbnail(url = user[2])
    # valueinfo exists so i can fit more stuff in value; no clue why f is needed before ""
    try:
        winRate = int((userRank[4] / (userRank[4] + userRank[5])) * 100)
        valueInfo = f"| {userRank[1]} {userRank[2]} | LP: {userRank[3]} | W: {userRank[4]} | L: {userRank[5]} | Winrate: {winRate}% |"
        embed.add_field(name = "Ranked Solo/Duo", value = valueInfo, inline = False)
    except:
        embed.add_field(name = "Ranked Solo/Duo not found", value = "No matches were found", inline = True)
    try:
        winRate = int((userRank[10] / (userRank[10] + userRank[11])) * 100)
        valueInfo = f"| {userRank[7]} {userRank[8]} | LP: {userRank[9]} | W: {userRank[10]} | L: {userRank[11]} | Winrate: {winRate}% |"
        embed.add_field(name = "Ranked Flex", value = valueInfo, inline = False)
    except:
        embed.add_field(name = "Ranked Flex not found", value = "No matches were found", inline = True)
    await ctx.send(embed = embed)


@bot.command()
async def euw(ctx, *nameWithSpace):
    name = formatter(nameWithSpace)
    user = profile("euw", name)
    userRank = rank("euw", user[3])
    embed = discord.Embed(title = user[0], description = user[1], color = 0xA5240C)
    embed.set_thumbnail(url = user[2])
    try:
        winRate = int((userRank[4] / (userRank[4] + userRank[5])) * 100)
        valueInfo = f"| {userRank[1]} {userRank[2]} | LP: {userRank[3]} | W: {userRank[4]} | L: {userRank[5]} | Winrate: {winRate}% |"
        embed.add_field(name = userRank[0], value = valueInfo, inline = False)
    except:
        embed.add_field(name = userRank[0] + " not found", value = "No matches were found", inline = True)
    try:
        winRate = int((userRank[10] / (userRank[10] + userRank[11])) * 100)
        valueInfo = f"| {userRank[7]} {userRank[8]} | LP: {userRank[9]} | W: {userRank[10]} | L: {userRank[11]} | Winrate: {winRate}% |"
        embed.add_field(name = userRank[6], value = valueInfo, inline = False)
    except:
        embed.add_field(name = " not found", value = "No matches were found", inline = True)
    await ctx.send(embed = embed)


@bot.command()
async def kr(ctx, *nameWithSpace):
    name = formatter(nameWithSpace)
    user = profile("kr", name)
    userRank = rank("kr", user[3])
    embed = discord.Embed(title = user[0], description = user[1], color = 0xA5240C)
    embed.set_thumbnail(url = user[2])
    try:
        winRate = int((userRank[4] / (userRank[4] + userRank[5])) * 100)
        valueInfo = f"| {userRank[1]} {userRank[2]} | LP: {userRank[3]} | W: {userRank[4]} | L: {userRank[5]} | Winrate: {winRate}% |"
        embed.add_field(name = userRank[0], value = valueInfo, inline = False)
    except:
        embed.add_field(name = "Ranked Solo/Duo not found", value = "No matches were found", inline = True)
    try:
        winRate = int((userRank[10] / (userRank[10] + userRank[11])) * 100)
        valueInfo = f"| {userRank[7]} {userRank[8]} | LP: {userRank[9]} | W: {userRank[10]} | L: {userRank[11]} | Winrate: {winRate}% |"
        embed.add_field(name = userRank[6], value = valueInfo, inline = False)
    except:
        embed.add_field(name = "Ranked Flex not found", value = "No matches were found", inline = True)
    await ctx.send(embed = embed)


@bot.event
async def on_ready():
    print('ready')


bot.run(discordToken)
