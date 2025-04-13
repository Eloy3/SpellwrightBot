import discord
from discord.ext import commands
from discord import app_commands
from spell_lookup import fetch_spell
from config import BOT_TOKEN

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def spell(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    spell_data = await fetch_spell(name)
    if spell_data:
        embed = discord.Embed(
            title=f"{spell_data['name']} (Level {spell_data['level']} {spell_data['school']})",
            description=spell_data['desc'],
            color=discord.Color.blue()
        )
        embed.add_field(name="Casting Time", value=spell_data['casting_time'], inline=True)
        embed.add_field(name="Range", value=spell_data['range'], inline=True)
        embed.add_field(name="Duration", value=spell_data['duration'], inline=True)
        embed.add_field(name="Components", value=", ".join(spell_data['components']), inline=True)
        embed.add_field(name="Ritual", value="Yes" if spell_data['ritual'] else "No", inline=True)
        embed.add_field(name="Concentration", value="Yes" if spell_data['concentration'] else "No", inline=True)
        embed.add_field(name="Higher Level", value=spell_data['higher_level'], inline=False)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(f"Spell '{name}' not found.")

spell_cmd = app_commands.Command(
    name="spell",
    description="Look up a D&D 5e spell by name.",
    callback=spell
)

@bot.event
async def on_ready():
    bot.tree.add_command(spell_cmd)
    await bot.tree.sync()

bot.run(BOT_TOKEN)
