import os
from io import BytesIO
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, File
from discord import Member
from PIL import Image, ImageDraw, ImageFont
import requests

# Load token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = Intents.default()
intents.message_content = True
intents.members = True  # Ensure to enable the members intent to track member join events

client = commands.Bot(command_prefix='!', intents=intents)

# Startup
@client.event
async def on_ready() -> None:
    await client.tree.sync()  # Sync commands with Discord
    print(f'{client.user} is now running!')

# Main entry point
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
