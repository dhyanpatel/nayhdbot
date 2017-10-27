from discord.ext import commands

Bot = commands.Bot(command_prefix='+', description='<Bot Name>")

# This creates the Bot! With this you can do the commands extension.

                   
#This is an example commmand to see 
@bot.command(pass_context = True, aliases = ['Ping'])
async def ping(ctx):
    """Pings the Discord servers and returns the response time."""
    await bot.send_typing(ctx.message.channel)
    startTime = time.monotonic()
    await (await bot.ws.ping())
    endTime = time.monotonic()
    ping = (endTime - startTime) * 1000
    await bot.say('The server response time was {}ms'.format(int(ping)))
