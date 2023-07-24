import json

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
            leaderboard[member.id] = {"total_time": 0, "start_time": datetime.utcnow()}
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


def load_leaderboard():
    global leaderboard
    try:
        with open('leaderboard.json', 'r') as file:
            leaderboard = json.load(file)
            print(leaderboard)
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
