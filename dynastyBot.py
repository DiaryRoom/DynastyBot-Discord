# Work with Python 3.6
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# discord bot token
TOKEN = "Njk2NTg5Mjk3NTQwNzkyMzMw.Xp935A.x-bOTxh97wgnQR0npERaaeAdjOs"

# google API credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('authentification.json', scope)

gc = gspread.authorize(creds)
# opens googles spreadsheet
sheet_qb = gc.open('discord test').sheet1
data_qb = sheet_qb.get_all_records()
sheet_rb = gc.open('discord test').get_worksheet(1)
data_rb = sheet_rb.get_all_records()

#####
# Below is all Discord bot server stuff
#####
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        #await client.send_message(message.channel, msg)

    if message.content.startswith('!contract'):
        cmd = message.content.split()
        # command will always be !contract [position] [first name] [last name] ([first name] [last name])

        msg = "Player(s) not found"

        # if only looking up one player
        if len(cmd) == 4:
            
            pos = []
            if cmd[1] == "qb":
                pos = data_qb
            else:
                pos = data_rb

            for x in pos:
                if x["Name"].split()[0] == cmd[2] and x["Name"].split()[1] == cmd[3]:

                    curr_year = 2020
                    status = x[str(curr_year)]

                    full_contract = "***" + x["Name"].split()[0] + " " + x["Name"].split()[1] + ", " + x["Name"].split()[2] + "***\n"

                    full_contract += (str(curr_year) + ": " + status + "\n")

                    while True:
                        if status == "UFA" or curr_year == 2025:
                            msg = full_contract
                            break

                        curr_year += 1
                        status = x[str(curr_year)]

                        full_contract += (str(curr_year) + ": " + status + "\n")

                    break

        elif len(cmd) > 4:

            pos = []

            if cmd[1] == "qb":
                pos = data_qb
            else:
                pos = data_rb

            comp = ""

            players = int((len(cmd) - 2) / 2)

            # first player
            for p in range(players):
                for x in pos:
                    if x["Name"].split()[0] == cmd[2 + (p * 2)] and x["Name"].split()[1] == cmd[3 + (p * 2)]:

                        curr_year = 2020
                        status = x[str(curr_year)]

                        full_contract = "***" + x["Name"].split()[0] + " " + x["Name"].split()[1] + ", " + x["Name"].split()[2] + "***\n"

                        full_contract += (str(curr_year) + ": " + status + "\n")

                        while True:
                            if status == "UFA" or curr_year == 2025:
                                comp += full_contract

                                break

                            curr_year += 1
                            status = x[str(curr_year)]

                            full_contract += (str(curr_year) + ": " + status + "\n")

            msg = comp

        else:
            msg = "Error: command must consist of !contract [position] [first name] [last name]"

        #msg = (sheet.cell(3,1).value).format(message)

        await message.channel.send(msg)

    if message.content.startswith('!help'):
        msg = 'oof'
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)