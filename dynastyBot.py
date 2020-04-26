# Work with Python 3.6
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import json

# discord bot token
with open('token.json','r') as f:
    # json file is just one entry with "Token" as the key, discord bot token as value
    TOKEN = json.load(f)["Token"]

# google API credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('authentification.json', scope)

# opens googles spreadsheet client
gc = gspread.authorize(creds)

# loads all google sheet data for all positions
sheet_qb = gc.open('Football Dynasty Contracts').get_worksheet(1)
# data_[position] indicates list of all data
data_qb = sheet_qb.get_all_values()
sheet_rb = gc.open('Football Dynasty Contracts').get_worksheet(2)
data_rb = sheet_rb.get_all_values()
sheet_wr = gc.open('Football Dynasty Contracts').get_worksheet(3)
data_wr = sheet_wr.get_all_values()
sheet_te = gc.open('Football Dynasty Contracts').get_worksheet(4)
data_te = sheet_te.get_all_values()

#####
# Below is all Discord bot server stuff
#####
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # temporary
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    # contract bot algorithm
    if message.content.startswith('!contract'):
        cmd = message.content.split()
        # command will always be !contract [position] [first name] [last name] ([first name] [last name])

        msg = "" # what the bot will ultimately output

        # if valid command
        if (len(cmd) >= 4 and len(cmd) % 2 == 0):
            pos = []

            # parse bot command to see what position
            if cmd[1] == "qb":
                pos = data_qb
            elif cmd[1] == "rb":
                pos = data_rb
            elif cmd[1] == "wr":
                pos = data_wr
            elif cmd[1] == "te":
                pos = data_te
            else:
                # if invalid position is input
                msg = "Error: invalid position"
                await message.channel.send(msg)
                return

            # string that will be built and ultimately sent as the bot message
            comp = ""

            # find number of players in bot command
            players = int((len(cmd) - 2) / 2)

            # bool to check if any input player name is invalid
            invalid_name = False

            # loops through the number of players to grab all necessary data
            for p in range(players):
                # bool to check if each player is ultimately found in google sheet
                found = False
                # checks if name exists in sheet
                for idx, x in enumerate(pos):
                    # first index is "[first name] [last name] [age]", parse to see if lines up with bot command
                    vals = x[0].split()
                    # checks if first name and last name exist in data
                    if (vals and idx > 3 and
                            (vals[0] == cmd[2 + (p * 2)] and vals[1] == cmd[3 + (p * 2)])):

                        found = True

                        curr_year = 2020

                        full_contract = ""

                        # loop through list of contract data for that player
                        for i, status in enumerate(x):
                            # first index will be name
                            if i == 0:
                                full_contract = "***" + status + "***\n"
                            # other indices will consist of contract data
                            else:
                                if not x[i]:
                                    full_contract += str(curr_year) + ": Under Contract\n"
                                else:
                                    full_contract += str(curr_year) + ": " + status + "\n"

                                # once there is a UFA or year is 2025, break the loop since no more data
                                if status == "UFA" or curr_year == 2025:
                                    comp += full_contract
                                    break

                                curr_year += 1

                if not found:
                    invalid_name = True
                    break

            if invalid_name:
                msg = "Error: invalid player name"
            else:
                msg = comp

        # invalid command - no position or incomplete name(s)
        else:
            msg = "Error: command must consist of !contract [position] [first name] [last name]"

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

#######
# OLD METHOD #
#######

# sheet_qb = gc.open('discord test').sheet1
# data_qb = sheet_qb.get_all_records()
# sheet_rb = gc.open('discord test').get_worksheet(1)
# data_rb = sheet_rb.get_all_records()

# for p in range(players):
#     # checks if name exists in sheet
#     found = False
#     # loops through data
#     for x in pos:
#         if x["Name"].split()[0] == cmd[2 + (p * 2)] and x["Name"].split()[1] == cmd[3 + (p * 2)]:

#             found = True

#             curr_year = 2020
#             status = x[str(curr_year)]

#             full_contract = "***" + x["Name"].split()[0] + " " + x["Name"].split()[1] + ", " + x["Name"].split()[2] + "***\n"

#             full_contract += (str(curr_year) + ": " + status + "\n")

#             while True:
#                 if status == "UFA" or curr_year == 2025:
#                     comp += full_contract

#                     break

#                 curr_year += 1
#                 status = x[str(curr_year)]

#                 full_contract += (str(curr_year) + ": " + status + "\n")

#     if not found:
#         invalid_name = True
#         break

# if invalid_name:
#     msg = "Error: invalid player name"
# else:
#     msg = comp