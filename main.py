import discord
from discord import app_commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot logged in as {client.user}")


@tree.command(name="getbadges", description="Get badges Hypesquad")
async def get_badges(interaction: discord.Interaction, token: str, house_id: int):

    if house_id not in [1, 2, 3]:
        await interaction.response.send_message("Invalid house_id (1,2,3 only)",ephemeral=True)
        return

    await interaction.response.send_message("Getting badges please wait...",ephemeral=True)

    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        data = {"house_id": house_id}

        response = requests.post(
            "https://discord.com/api/v9/hypesquad/online",
            headers=headers,
            json=data
        )

        if response.status_code == 204:
            await interaction.followup.send("Đổi HypeSquad thành công!",ephemeral=True)
        elif response.status_code == 400:
            await interaction.followup.send("Token không hợp lệ hoặc đã hết hạn",ephemeral=True)
        elif response.status_code == 401:
            await interaction.followup.send("Token Sai",ephemeral=True)
        elif response.status_code == 429:
            await interaction.followup.send("Bị giới hạn tốc độ, thử lại sau",ephemeral=True)
        else:
            await interaction.followup.send(f"Lỗi {response.status_code}",ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"Lỗi: {str(e)}",ephemeral=True)


@tree.command(name="getinfo", description="Get info user")
async def get_info(interaction: discord.Interaction, user: discord.User):

    created_at = int(user.created_at.timestamp())

    avatar = user.display_avatar.url if user.display_avatar else None

    embed = discord.Embed(
        title="User Information",
        color=discord.Color.blue()
    )

    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="User ID", value=user.id, inline=True)
    embed.add_field(name="Bot", value="Yes" if user.bot else "No", inline=True)
    embed.add_field(name="Account Created", value=f"<t:{created_at}:D>", inline=False)

    if avatar:
        embed.set_thumbnail(url=avatar)

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

client.run(TOKEN)
