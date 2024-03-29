import discord
import Create_Message
from Environment_Variables import *

client = discord.Client()
DISCORD_TOKEN = DISCORD_TOKEN


# discord recommends using bigint's to store the permissions for your bot
# use by OR'ing hex values together 
PERMISSION_SEND_MESSAGES = 0x40
PERMISSION_USE_EXTERNAL_EMOJIS = 0x40000
PERMISSION_CONNECT = 0x100000
PERMISSION_SPEAK = 0x200000
PERMISSION_USE_APP_COMMANDS = 0x80000000

permissions = PERMISSION_SEND_MESSAGES | PERMISSION_USE_EXTERNAL_EMOJIS | PERMISSION_CONNECT | PERMISSION_SPEAK | PERMISSION_USE_APP_COMMANDS


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

# simple login print statement to console
@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))

# function for sending messages 
@client.event
async def on_message(message:str) -> None:
        
    if message.author == client.user:
        return

    msg_txt = Create_Message.chat(message.content)

    if msg_txt == "Goodbye!":
        await message.channel.send(msg_txt)
        await client.close()

    # loop that sends messages until the msg buffer is empty
    while len(msg_txt) > 0:
        index_sep = separate_msg(msg_txt)
        await message.channel.send(msg_txt[0:index_sep])
        msg_txt = msg_txt[index_sep:].strip() # get rid of any extra white space
    

client.run(DISCORD_TOKEN)  # local version, do not share
# client.run(os.getenv('TOKEN')) for non local versions
