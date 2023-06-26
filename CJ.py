from typing import Optional
import discord
from discord.ext import commands, tasks
import asyncio
from discord import Activity, ActivityType
from datetime import datetime
from discord.interactions import Interaction
import pytz

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())
category_id = 1121938332562247871
channel_name = "f{self.user}"



@bot.event
async def on_ready():
    print("bot connecté")
    custom_status = "Hello, I'm a Discord bot!"
    activity = Activity(type=ActivityType.custom, name=custom_status)
    await bot.change_presence(activity=activity)
    #await bot.tree.sync()
    print('Command tree synced.')

@bot.event
async def on_guild_available(guild):
    print(f"Le serveur '{guild.name}' est disponible.")


@tasks.loop(minutes=1)  # Exécute la commande toutes les 5 minutes
async def sort_channels_in_category(ctx):
    guild = ctx.guild

    # Récupère la catégorie "CASIERS"
    target_category_name = "CASIERS"
    target_category = discord.utils.get(guild.categories, name=target_category_name)

    if not target_category:
        await ctx.send(f"La catégorie spécifiée '{target_category_name}' n'a pas été trouvée dans ce serveur.")
        return

    # Récupère les canaux de la catégorie "CASIERS"
    channels_in_category = target_category.channels

    # Trie les canaux par ordre alphabétique
    sorted_channels = sorted(channels_in_category, key=lambda c: c.name)

    # Réorganise les canaux dans la catégorie
    for index, channel in enumerate(sorted_channels):
        await channel.edit(position=index)

    await ctx.send("Les canaux dans la catégorie 'CASIERS' ont été triés par ordre alphabétique.")


class RepportModal(discord.ui.Modal, title="CASIER"):
    user = discord.ui.TextInput(label="Nom", placeholder="Nom Prénom", required=True, max_length=100, style=discord.TextStyle.short)
    agent = discord.ui.TextInput(label="Agents Présents :", placeholder="13,14,29,53...", required=True, max_length=100, style=discord.TextStyle.short)
    cost = discord.ui.TextInput(label="Ammende", placeholder="100k$", required=True, max_length=100, style=discord.TextStyle.short)
    why = discord.ui.TextInput(label="motif", placeholder="refus d'obtempérer délit de fuite", required=True, max_length=100, style=discord.TextStyle.short)
    more = discord.ui.TextInput(label="infosup(temps de GAV autres)", placeholder=" - Temps de GAV :  \n - Informations supplémentaires :", required=True, max_length=2000, style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):
        paris_timezone = pytz.timezone("Europe/Paris")
        current_time = datetime.now(paris_timezone).strftime("%d-%m-%Y %H:%M:%S")

        target_category_name = "CASIERS"
        target_category = discord.utils.get(interaction.guild.categories, name=target_category_name)
        channel_name = self.user.value.replace(" ", "-").lower()
        print(channel_name)
            # Check if the channel exists
        existing_channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        if existing_channel:
            embed = discord.Embed(title=f"Mise a jour", color=discord.Color.red())
            embed.set_footer(text=f"Mis a jour le : {current_time}")
            embed.add_field(name=" 👮 │ Agents Présents :", value=self.agent, inline=False)
            embed.add_field(name=" 💵  | Amende :", value=self.cost, inline=False)
            embed.add_field(name=" 📄 │ Motifs :", value=self.why, inline=False)
            embed.add_field(name="⚠️ │Informations supplémentaires :", value=f"{self.more}", inline=False)


            await existing_channel.send(content=interaction.user.mention, embed=embed)
            await interaction.response.send_message(f"CASIER JUDICIARE fait par {interaction.user.mention} \n 👤 │ Identité du suspect : {self.user} \n 👮 │ Agents Présents : {self.agent} \n 💵  | Amende : {self.cost} \n 📄 │ Motifs : {self.why} \n ⚠️ │Informations supplémentaires : {self.more}",ephemeral=True)

        else:
        # Create a new channel
            new_channel = await interaction.guild.create_text_channel(channel_name, category=target_category)
            embed = discord.Embed(title=f"CASIER JUDICIAIRE ", color=discord.Color.red())
            embed.set_footer(text=f"crée le : {current_time}")
            embed.add_field(name=" 👤 │ Identité du suspect :", value=self.user, inline=False)
            embed.add_field(name=" 👮 │ Agents Présents :", value=self.agent, inline=False)
            embed.add_field(name=" 💵  | Amende :", value=self.cost, inline=False)
            embed.add_field(name=" 📄 │ Motifs :", value=self.why, inline=False)
            embed.add_field(name="⚠️ │Informations supplémentaires :", value=self.more, inline=False)
            await new_channel.send(content=interaction.user.mention, embed=embed)
            await interaction.response.send_message(f"CASIER JUDICIARE fait par {interaction.user.mention} \n 👤 │ Identité du suspect : {self.user} \n 👮 │ Agents Présents : {self.agent} \n 💵  | Amende : {self.cost} \n 📄 │ Motifs : {self.why} \n ⚠️ │Informations supplémentaires : {self.more}",ephemeral=True)


@bot.tree.command(name="casier", description="créer un casier")
async def casier(interaction: discord.Interaction):
    await interaction.response.send_modal(RepportModal())

class celluleModal(discord.ui.Modal, title="Mise en Cellule"):
    paris_timezone = pytz.timezone("Europe/Paris")
    current_time = datetime.now(paris_timezone).strftime("%d/%m/%Y %H:%M")
    nom = discord.ui.TextInput(label="Nom", placeholder="Nom Prénom", required=True, max_length=100, style=discord.TextStyle.short)
    hehs = discord.ui.TextInput(label="Date / Heure (entrée - sortie)", placeholder=f"{current_time} - heure de sortie ", required=True, max_length=100, style=discord.TextStyle.short)
    tt = discord.ui.TextInput(label="temps de prison", placeholder="20 minutes", required=True, max_length=100, style=discord.TextStyle.short)
    tool = discord.ui.TextInput(label="Objets saisis", placeholder="ex: berretta", required=False, max_length=100, style=discord.TextStyle.short)
    what = discord.ui.TextInput(label="faits reprochés :", placeholder="ex: braquage magasin", required=True, max_length=2000, style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):
        channel = discord.utils.get(interaction.guild.channels, name="mise-en-cellule")
            
        embed = discord.Embed(title=f"Mise en Cellule", color=discord.Color.blurple())
        embed.add_field(name=" Nom Prénom :", value=self.nom, inline=False)
        embed.add_field(name="Date / Heure (entrée - sortie):", value=self.hehs, inline=False)
        embed.add_field(name="temps de prison :", value=self.tt, inline=False)
        embed.add_field(name="Objets saisis :", value=self.tool, inline=False)
        embed.add_field(name="faits reprochés :", value=self.what, inline=False)
        await channel.send(content=interaction.user.mention, embed=embed)
        await interaction.response.send_message(f"mise en cellule fait par {interaction.user.mention} \n 👤 │ Identité du suspect : {self.nom} \n 📅 │ Date du casier judiciaire : {self.hehs} \n 💵  | Amende : {self.tt} \n 📄 │ Motifs : {self.tool} \n ⚠️ │Informations supplémentaires : {self.what}",ephemeral=True)

@bot.tree.command(name="cellule", description="faire une mise en cellule")
async def cellule(interaction: discord.Interaction):
    await interaction.response.send_modal(celluleModal())

@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')
    await ctx.send('You must be the owner to use this command!')

bot.run("")
