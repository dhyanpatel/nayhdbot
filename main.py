import discord, random, pyowm, asyncio
from discord.ext import commands

# for handling request errors
from urllib.error import HTTPError

#--------------------------------------------------------------------------

owm = pyowm.OWM('3efe1d1446293d1db9d885956d91ebf5')

#--------------------------------------------------------------------------

description = "This is Dhyan's Test Discord Bot"
client = discord.Client()
global pollholder
pollholder = []
unique_dict = {}
#--------------------------------------------------------------------------

#When client starts up
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print (description)
    print(client.user.id)
    print (list(client.servers))
    await client.change_presence(game=discord.Game(name='Codeday Presentation'))
    print('---------')
#--------------------------------------------------------------------------

#Commands
@client.event
async def on_message(message):
    split = message.content.split()
    if split[0] == "!ping":
        await client.send_message(message.channel, "pong")
#--------------------------------------------------------------------------

    elif split[0] == "!roll":
        try:
            x = split[1]
            y = split[2]
            await client.send_message(message.channel, str(random.randint(int(x),int(y))))
        except (ValueError,IndexError):
            await client.send_message(message.channel, "Fuck you, use !roll x y. With x and y being integers.")
#--------------------------------------------------------------------------

    elif split[0] == "!weather":
        try:
            observation = owm.weather_at_place(" ".join(split[1:]))
            weather = observation.get_weather()
            wind = weather.get_wind()
            humidity = weather.get_humidity()
            heat = weather.get_temperature('fahrenheit')
            formatted_weather = "| Wind speed is: "+str(wind['speed']) + "m/s| Humidity is: " + str(humidity) + "%| Heat is: " + str(heat['temp']) + " Degrees Fahrenheit|  --- in " + " ".join(split[1:])
            await client.send_message(message.channel, formatted_weather)
        except Exception:
            await client.send_message(message.channel, "Fuck you, that's not a place")
#--------------------------------------------------------------------------

    elif split[0] == "!say":
        send = ' '.join(split[1:])
        await client.send_message(message.channel, send)
#--------------------------------------------------------------------------

    elif split[0] == "!clear":
        try:
            if str(message.channel) != "general":
                deleted = await client.purge_from(message.channel)
                await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
            else:
                deleted = await client.purge_from(message.channel, limit = 1)
                await client.send_message(message.channel, "Can't use this command in #general")
        except (HTTPException):
            deleted = await client.purge_from(message.channel, limit = 1)
            await client.send_message(message.channel, "Can't delete messages older than 14 days.")
#--------------------------------------------------------------------------

    elif split[0] == "!math":
        try:
            answer = eval("".join(split[1:]))
            await client.send_message(message.channel, answer)
        except IndexError:
            await client.send_message(message.channel, "Couldn't evaluate")
#--------------------------------------------------------------------------
    elif split[0] == "!poll":
        try:
            global pollholder
            if split[1] == "newpoll":
                pollholder = []
            if split[1] == "addvote":
                pollholder.append(split[2])
                await client.send_message(message.channel, split[2] + " Was Added")
            if split[1] == "results":
                await client.send_message(message.channel, str(pollholder))
                temp = []
                for iteration in pollholder:
                    if iteration not in temp:
                        temp.append(iteration)
                for iteration in temp:
                    unique_dict[iteration] = pollholder.count(iteration)
                await client.send_message(message.channel, str(unique_dict))
        except (IndexError, UnboundLocalError):
            await client.send_message(message.channel, "Not enough arguments, or Newpoll not made")



client.run('Token')

