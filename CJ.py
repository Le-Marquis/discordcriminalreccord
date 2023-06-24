from typing import Optional
import discord
from discord.ext import commands
import asyncio
import os

from discord.interactions import Interaction

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())


@bot.event
async def on_ready():
    print("bot connecté")

async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    
    if existing_channel:
        await ctx.send(f"The channel {channel_name} already exists.")
    else:
        await guild.create_text_channel(channel_name)
        await ctx.send(f"The channel {channel_name} has been created.")
        await ctx.messages.delete()

class RepportModal(discord.ui.Modal, title="Casier Judiciare"):
    user = discord.ui.TextInput(label="Nom Prénom", placeholder="ex John Smith", required=True, max_length=100, style=discord.TextStyle.short)
    date = discord.ui.TextInput(label="date", placeholder="20/06/2023", required=True, max_length=100, style=discord.TextStyle.short)
    cost = discord.ui.TextInput(label="ammende", placeholder="100k$", required=True, max_length=100, style=discord.TextStyle.short)
    why = discord.ui.TextInput(label="motif", placeholder="refus d'obtempérer délit de fuite", required=True, max_length=100, style=discord.TextStyle.short)
    more = discord.ui.TextInput(label="infosup( agents presents temps de GAV autres)", placeholder=".....", required=True, max_length=2000, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction, user):
        channel_name = user
        channel = interaction.utils.get(interaction.guild.channels, name=channel_name)
            
        if channel:
             await interaction.response.send_message(f"CASIER JUDICIARE  \n 👤 │ Identité du suspect : {self.user} \n 📅 │ Date du casier judiciaire : {self.date} \n 💵  | Amende : {self.cost} \n 📄 │ Motifs : {self.why} \n ⚠️ │Informations supplémentaires : {self.more}")
        else:
            await interaction.create_text_channel(channel_name)
            await interaction.response.send_message(f"CASIER JUDICIARE  \n 👤 │ Identité du suspect : {self.user} \n 📅 │ Date du casier judiciaire : {self.date} \n 💵  | Amende : {self.cost} \n 📄 │ Motifs : {self.why} \n ⚠️ │Informations supplémentaires : {self.more}")


@bot.tree.command(name="casier", description="creer un casier")
async def casier(interaction: discord.Interaction):
    await interaction.response.send_modal(RepportModal())

async def main():
    async with bot:
        await bot.start("MTEyMjA4MzAyOTY2MjMxNDU4Ng.GSAnBW.36tcaB3xo-SnYq-E1cffEwAJa4cPswpSlXVarE")
    
asyncio.run(main())

#class InvitationButton(discord.ui.View):
#    def __init__(self, inv: str):
#       super().__init__()
#        self.inv = inv
#        self.add_item(discord.ui.Button(Label="Invite link"))
    
#@discord.ui.Button(label="Invite btn", style=discord.ui.ButtonStyle.blurple)
#async def inviteBtn(self, ctx: interaction: discord.Interaction, button: discord.ui.Button):
#    await ctx.interaction.response.send_modal(RepportModal())
