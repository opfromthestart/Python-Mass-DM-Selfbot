import discum
import json
import os.path
import random
import time
from rich import print


def load_from_data_else_ask(field, message):
    global data
    if data is not None and field in data.keys():
        return data[field]
    return input(message)


data = None
if os.path.exists("data.json"):
    data = json.loads(open("data.json").read())
if data is not None and "token" in data.keys():
    token = data["token"]
else:
    token = input('ur token: ')
bot = discum.Client(token=token, log=False)
memberz = []
guildz = load_from_data_else_ask("guildid", "Please input guild ID: ")
if data is not None and "channelids" in data.keys():
    channelz = data["channelids"]
else:
    channelz = [load_from_data_else_ask("channelid", "Please input a channel ID in that guild: ")]
if data is not None and "messages" in data.keys():
    messagz = data["messages"]
else:
    messagz = [load_from_data_else_ask("message", "Please input your message: ")]
timez = load_from_data_else_ask("time", "How long between DMs: ")
if data is not None and "ignoreRoles" in data.keys():
    ignores = data["ignoreRoles"]
else:
    ignores = []
if data is not None and "onlyRoles" in data.keys():
    roles = data["onlyRoles"]
else:
    roles = None


@bot.gateway.command
def memberTest(resp):
    if resp.event.ready_supplemental:
        for channel in channelz:
            bot.gateway.fetchMembers(guildz, channel)
    if bot.gateway.finishedMemberFetching(guildz):
        bot.gateway.removeCommand(memberTest)
        bot.gateway.close()


bot.gateway.run()
badMemberz = set()
onlyMemberz = set()
print("Getting members not to message")
for role in ignores:
    for mem in bot.getRoleMemberIDs(guildz, role).json():
        badMemberz.add(mem)
for role in roles:
    for mem in bot.getRoleMemberIDs(guildz, role).json():
        onlyMemberz.add(mem)
print("Starting add members.")
for memberID in bot.gateway.session.guild(guildz).members:
    if roles is None:
        memberz.append(memberID)
    elif memberID in onlyMemberz:
        memberz.append(memberID)
for mem in memberz:
    if mem in badMemberz:
        memberz.remove(mem)
print("Starting to DM. Members:", len(memberz))
abort = input("abort?")
if abort != "no":
    exit(1)
for x in memberz:
    try:
        rand = random.randint(0, 20)
        if rand == 20:
            print(f'Sleeping for 45 seconds to prevent rate-limiting.')
            time.sleep(45)
            print(f'Done sleeping!')
        print(f"Preparing to DM {x}.")
        time.sleep(int(timez))
        newDM = bot.createDM([f"{x}"]).json()["id"]
        bot.sendMessage(newDM,
                        f"{random.choice(messagz)} DM bot by https://github.com/Apophis52/Python-Mass-DM-Selfbot/")
        print(f'DMed {x}.')
    except Exception as E:
        print(E)
        print(f'Couldn\'t DM {x}.')
