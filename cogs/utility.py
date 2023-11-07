from discord.ext import commands
from discord import app_commands
from pathlib import Path
from helpers.checks import missingPermissions
import json
import time

# This cog is for general commands eg. shutdown, toggle, status

currentDir = Path(__file__).resolve().parent
parrent = currentDir.parent
configLocation = parrent / "config.json"

with open(configLocation, "r") as file:
    config = json.load(file)

def currentTime():
    return time.strftime("%H:%M:%S", time.localtime())

# --------- #

class Utility(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog: {__name__} has loaded")
    
    # --------- #

    @app_commands.command(
        name = "toggle",
        description = "This enables or disables the link fixer")
    async def togglefixer(self, interaction):
        if interaction.user.id == int(config["admin"]):
            config['enabled'] = not config['enabled']
            with open(configLocation, 'w') as f:
                json.dump(config, f, indent=4)
            
            await interaction.response.send_message(f"Toggled to {config['enabled']}", ephemeral=True)
            print(f"Toggled to: {config['enabled']}@{currentTime()}")
        else:
            await missingPermissions(interaction)

    # --------- #

    @app_commands.command(
            name= "shutdown",
            description = "turns off the bot!")
    async def shutdown(self, interaction):
        if interaction.user.id == int(config["admin"]):
            await interaction.response.send_message("Shutting down...", delete_after=3.0, ephemeral=True)
            print(f"Bot offline@{currentTime()}")
            await self.client.close()
        else:
            await missingPermissions(interaction)

# --------- #

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Utility(client))