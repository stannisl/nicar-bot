import discord
from discord import app_commands
from locales.locales import get_localized_text
from handlers.views import create_language_view
from handlers.sessions import user_sessions

@app_commands.command(name="verify", description="Начать процесс верификации Steam")
async def verify_command(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    if user_id in user_sessions:
        embed = discord.Embed(
            title=get_localized_text("RU", "active_session"),
            description=get_localized_text("RU", "active_session_desc"),
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title=get_localized_text("RU", "welcome"),
        description=get_localized_text("EN", "greeting"),
        color=0x0099ff
    )
    
    view = create_language_view()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@app_commands.command(name="help", description="Показать справку по командам")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title=get_localized_text("RU", "help_title"),
        description=get_localized_text("RU", "help_desc"),
        color=0x0099ff
    )
    
    commands = [
        ("/verify", "Начать процесс верификации Steam"),
        ("/help", "Показать эту справку"),
        ("/cancel", "Отменить текущую верификацию")
    ]
    
    for name, value in commands:
        embed.add_field(name=name, value=value, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@app_commands.command(name="cancel", description="Отменить текущую верификацию")
async def cancel_command(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    if user_id in user_sessions:
        lang = user_sessions[user_id]
        del user_sessions[user_id]
        
        embed = discord.Embed(
            title=get_localized_text(lang, "cancel"),
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=get_localized_text("RU", "no_session"),
            description=get_localized_text("RU", "no_session_desc"),
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)