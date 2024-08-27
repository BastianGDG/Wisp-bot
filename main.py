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

# Generate Welcome Banner
def generate_welcome_banner(member: Member):
    # Load base image
    base = Image.open(r"C:\Users\theco\Downloads\Wisp bot\Wisp_Cyan.png").convert("RGBA")
    
    # Fetch the member's avatar
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")

    # Resize the avatar
    avatar = avatar.resize((150, 150))  # Adjust size as needed
    
    # Position the avatar on the banner
    base.paste(avatar, (100, 50), avatar)  # Adjust position as needed

    # Add welcome text
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("arial.ttf", 40)  # Ensure this font is available, or provide a path to a TTF file
    text = f"Welcome, {member.name}!"
    text_position = (300, 100)  # Adjust position as needed
    draw.text(text_position, text, font=font, fill="white")

    # Save to a BytesIO object for sending without saving to disk
    image_binary = BytesIO()
    base.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# Event: on_member_join
@client.event
async def on_member_join(member: Member):
    # Generate the welcome banner
    banner = generate_welcome_banner(member)
    
    # Send the banner to a specific channel
    channel = client.get_channel(782681033727541311)  # Replace with your channel ID
    await channel.send(f"Welcome to the server, {member.mention}!", file=File(banner, 'welcome.png'))

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
