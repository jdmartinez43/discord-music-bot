import discord
import Create_Message

client = discord.Client()

# discord doesn't allow for messages to be longer than 2000 chars 
# so we use this to find what index in the string to split 
# the message by so the text is still readable
def separate_msg(msg:str) -> int:
    try:
        if msg[1999] == "\n":
            return 2000
        else:
            r = 1998
            while msg[r] != "\n":
                r -= 1
            return r + 1 
    except IndexError:
        return len(msg)

@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message:str) -> None:
        
    if message.author == client.user:
        return

    msg_txt = Create_Message.chat(message.content)

    if msg_txt == "Goodbye!":
        await message.channel.send(msg_txt)
        await client.close()

    while len(msg_txt) > 0:
        index_sep = separate_msg(msg_txt)
        await message.channel.send(msg_txt[0:index_sep])
        msg_txt = msg_txt[index_sep:].strip()
    

client.run("ODEzNjUzMTE0OTAwODQwNDQ4.YDSbgw.VntaalyhvUQL9h58SmnEDMwUejw")  # local version, do not share
# client.run(os.getenv('TOKEN')) for non local versions