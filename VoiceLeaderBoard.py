import json
from typing import Optional

import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio
from datetime import datetime, timedelta, timezone, time
import datetime as date
import os

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
BOT_TOKEN = "MTA5NzI1MjUxODk4NTIxNjIzMQ.GBAnDX.hX8bWBnM2GJKktEycHfu10fo6iahPQKQtXG3UY"
LAST_RESET_WEEK_FILE = "last_reset_week.txt"

leaderboard = {}


async def reset_leaderboard_weekly_task() -> None:
    while True:
        current_week = date.datetime.utcnow().isocalendar()[1]
        last_reset_week = load_last_reset_week()
        if current_week != last_reset_week:
            reset_leaderboard_weekly()
            channel = bot.get_channel(1122116231978295306)
            sorted_leaderboard = sorted(leaderboard.items(),
                                        key=lambda x: leaderboard[x[0]]["total_time"] if isinstance(leaderboard[x[0]],
                                                                                                    dict) else 0,
                                        reverse=True)
            embed = discord.Embed(title="Leaderboard", color=discord.Color.green())
            count = 0
            for index, (member_id, minutes) in enumerate(sorted_leaderboard):
                if member_id == "message":
                    continue
                if isinstance(leaderboard[member_id], dict):
                    time = leaderboard[member_id]["total_time"]
                    minutes = time // 60
                    count += 1
                    embed.add_field(name=f"{count}. {bot.get_user(int(member_id))}", value=f"{minutes} minutes",
                                    inline=False)

                print(str(count) + " - " + str(member_id) + " - " + str(minutes) + " minutes")
            message = await channel.send(embed=embed)
            leaderboard["message"] = message.id
        else:
            channel = bot.get_channel(1122116231978295306)
            sorted_leaderboard = sorted(leaderboard.items(),
                                        key=lambda x: leaderboard[x[0]]["total_time"] if isinstance(leaderboard[x[0]],
                                                                                                    dict) else 0,
                                        reverse=True)
            embed = discord.Embed(title="Leaderboard", color=discord.Color.green())
            count = 0
            for index, (member_id, minutes) in enumerate(sorted_leaderboard):
                if member_id == "message":
                    continue
                if isinstance(leaderboard[member_id], dict):
                    time = leaderboard[member_id]["total_time"]
                    minutes = time // 60
                    count += 1
                    embed.add_field(name=f"{count}. {bot.get_user(int(member_id))}", value=f"{minutes} minutes",
                                    inline=False)

                print(str(count) + " - " + str(member_id) + " - " + str(minutes) + " minutes")
            if leaderboard.get('message'):
                message = await channel.fetch_message(int(leaderboard.get('message')))
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                leaderboard["message"] = message.id
        save_leaderboard()
        await asyncio.sleep(30 * 60)


@bot.event
async def on_ready():
    print("Bot ist online")
    await bot.change_presence(status=discord.Status.online)

    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
    load_leaderboard()
    asyncio.create_task(reset_leaderboard_weekly_task())


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if member.id not in leaderboard:
            leaderboard[member.id] = {"total_time": 0, "member_name": member.name, "start_time": datetime.utcnow()}
        else:
            start_time = leaderboard[member.id]["start_time"]
            if "start_time" not in leaderboard[member.id] or leaderboard[member.id]["start_time"] is None:
                leaderboard[member.id]["start_time"] = datetime.utcnow()
    elif before.channel is not None and after.channel is None:
        if member.id in leaderboard and "start_time" in leaderboard[member.id] and leaderboard[member.id][
            "start_time"] is not None:
            start_time = leaderboard[member.id]["start_time"]
            time_in_channel = datetime.utcnow() - start_time
            rounded_time = round(time_in_channel.total_seconds())
            leaderboard[member.id]["total_time"] += rounded_time
            leaderboard[member.id]["start_time"] = None

    save_leaderboard()


@bot.tree.command(name="show_leaderboard", description="Show the current leaderboard.")
async def show_leaderboard(interaction: discord.Interaction):
    if interaction.channel.id != 1122116231978295306:
        await interaction.response.send_message("The command can only be performed in the time channel.")
        return
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["total_time"], reverse=True)
    embed = discord.Embed(title=f"Leaderboard TOP10:", color=discord.Color.green())
    count: int = 0
    for index, (member_id, data) in enumerate(sorted_leaderboard):
        if count >= 10: continue
        member = bot.get_user(member_id)
        minutes = data['total_time'] // 60
        embed.add_field(name=f"{index + 1}. {member}", value=f"{minutes} minutes")
        count += 1
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="stats", description="Show the current stats of a user.")
async def stats(interaction: discord.Interaction, user: discord.User):
    if interaction.channel.id != 1122116231978295306:
        await interaction.response.send_message("The command can only be performed in the time channel.")
        return
    member_id = user.id
    if member_id in leaderboard:
        time = leaderboard[member_id]["total_time"]
        minutes = time // 60
        embed = discord.Embed(title=f"{user}", description=f"Time: {minutes} minutes", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("This user was never in a talk on this discord.")


@bot.event
async def on_member_join(member):
    embed = discord.Embed(description=f"Hey {member.mention}, welcome to **FORTPLAYㄨ**!", color=discord.Color.green())
    embed.set_image(
        url="https://images-ext-2.discordapp.net/external/9CMDm4sNeGZItMzz1YZYMDwKoRykBa-rWH9CWP-ZWXc/https/cdn-longterm.mee6.xyz/plugins/welcome/images/1059749448986677260/b067546737aef6affb45369d6500b99519596f8dace4645bab54da3a09938e48.gif")
    await bot.get_channel(1059749449594830915).send(embed=embed)


@bot.tree.command(name="poll", description="You can create with this command a new poll.")
async def poll(interaction: discord.Interaction, question: str, answer1: Optional[str], answer2: Optional[str],
               answer3: Optional[str], answer4: Optional[str], answer5: Optional[str], answer6: Optional[str],
               answer7: Optional[str]):
    if interaction.user.guild_permissions.administrator:
        embed = discord.Embed(title="FORTPLAYㄨ", description=question, color=discord.Color.blue())
        answers = []
        if answer1 is not None:
            answers.append({"emoji": "1️⃣", "answer": ":one: " + answer1})
        if answer2 is not None:
            answers.append({"emoji": "2️⃣", "answer": ":two: " + answer2})
        if answer3 is not None:
            answers.append({"emoji": "3️⃣", "answer": ":three: " + answer3})
        if answer4 is not None:
            answers.append({"emoji": "4️⃣", "answer": ":four: " + answer4})
        if answer5 is not None:
            answers.append({"emoji": "5️⃣", "answer": ":five: " + answer5})
        if answer6 is not None:
            answers.append({"emoji": "6️⃣", "answer": ":six: " + answer6})
        if answer7 is not None:
            answers.append({"emoji": "7️⃣", "answer": ":seven: " + answer7})

        for answer in answers:
            embed.add_field(name=answer["answer"], value=" ", inline=False)

        await interaction.response.send_message("The poll is successfully created.", ephemeral=True)
        message = await interaction.channel.send(embed=embed)

        if message is not None:
            for answer in answers:
                if "one" in answer["answer"]:
                    await message.add_reaction("1️⃣")
                if "two" in answer["answer"]:
                    await message.add_reaction("2️⃣")
                if "three" in answer["answer"]:
                    await message.add_reaction("3️⃣")
                if "four" in answer["answer"]:
                    await message.add_reaction("4️⃣")
                if "five" in answer["answer"]:
                    await message.add_reaction("5️⃣")
                if "six" in answer["answer"]:
                    await message.add_reaction("6️⃣")
                if "seven" in answer["answer"]:
                    await message.add_reaction("7️⃣")
    else:
        await interaction.response.send_message("You dont have the permission to perform this command.")



@bot.tree.command(name="ticketsetup", description="You can create with this command a new ticket panel.")
async def ticketsetup(interaction: discord.Interaction, content: str, ticket_button: str):
    if interaction.user.guild_permissions.administrator:
        button = Button(label=ticket_button, style=discord.ButtonStyle.green, custom_id="ticket_button")
        view = View()
        view.add_item(button)
        embed = discord.Embed(description=content, color=discord.Color.green())
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("You have successfully created the ticket panel.", ephemeral=True)
    else:
        await interaction.response.send_message("You dont have the permission to perform this command.")


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if "ticket_button" in str(interaction.data):
        guild = bot.get_guild(1059749448986677260)

        category = bot.get_channel(1059749450240757803)
        ticket_channel = await guild.create_text_channel(f"🟠تذكرة - {interaction.user.name}",
                                                         category=category)

        await ticket_channel.set_permissions(guild.get_role(1059749448986677260), send_messages=False,
                                             read_messages=False, add_reactions=False,
                                             embed_links=False, attach_files=False, read_message_history=False,
                                             external_emojis=False)
        await ticket_channel.set_permissions(guild.get_role(1059749448986677262), send_messages=False,
                                             read_messages=False, add_reactions=False,
                                             embed_links=False, attach_files=False, read_message_history=False,
                                             external_emojis=False)
        await ticket_channel.set_permissions(guild.get_role(1060479179474341918), send_messages=True,
                                             read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=False, read_message_history=True,
                                             external_emojis=True)
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        embed = discord.Embed(
            description=f'Thank you for contacting support. \nPlease describe your issue and await a response.',
            color=discord.Color.green())
        button = Button(label="Close", style=discord.ButtonStyle.green, custom_id="ticket_close")
        view = View()
        view.add_item(button)
        await ticket_channel.send(embed=embed, view=view)
        await interaction.response.send_message(
            f'{ticket_channel.mention} تم فتح تذكرة جديدة:',
            ephemeral=True)
        return
    if "ticket_close" in str(interaction.data):
        if "🟠" in interaction.channel.name:
            embed = discord.Embed(description="The Ticket will close in 30 seconds.",
                                  color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(30)
            try:
                await interaction.channel.delete()
            except Exception as e:
                await interaction.channel.send("There is an error in deleting the ticket.")
        else:
            await interaction.response.send_message("You arent in a ticket.", ephemeral=True)
        return


@bot.tree.command(name="close", description="You can close with this command the ticket.")
async def close(interaction: discord.Interaction):
    if "🟠" in interaction.channel.name:
        embed = discord.Embed(description="The Ticket will close in 30 seconds.",
                              color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(30)
        try:
            await interaction.channel.delete()
        except Exception as e:
            await interaction.channel.send("There is an error in deleting the ticket.")
    else:
        await interaction.response.send_message("You arent in a ticket.", ephemeral=True)
    return


def load_leaderboard():
    global leaderboard
    try:
        with open('leaderboard.json', 'r') as file:
            leaderboard = json.load(file)
    except FileNotFoundError as e:
        print(e)
        leaderboard = {}


def save_leaderboard():
    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file, default=str)


def reset_leaderboard_weekly():
    current_week = date.datetime.utcnow().isocalendar()[1]
    last_reset_week = load_last_reset_week()
    if current_week != last_reset_week:
        leaderboard.clear()
        save_last_reset_week(current_week)
        save_leaderboard()


def load_last_reset_week():
    if os.path.exists(LAST_RESET_WEEK_FILE):
        with open(LAST_RESET_WEEK_FILE, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                pass
    return 0


def save_last_reset_week(week):
    with open(LAST_RESET_WEEK_FILE, "w") as file:
        file.write(str(week))


bot.run(BOT_TOKEN)
