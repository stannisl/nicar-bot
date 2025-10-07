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
        title=get_localized_text("EN", "welcome"),
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

@app_commands.command(name="start_verify", description="Начать верификацию для пользователя (только для админов)")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def ls_command(interaction: discord.Interaction, user: discord.User):
    """Команда для админов - запуск верификации для указанного пользователя"""
    from handlers.views import create_language_view
    from locales.locales import get_localized_text
    
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Ошибка",
            description="У вас нет прав для использования этой команды",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Проверяем активную сессию
    if user.id in user_sessions:
        embed = discord.Embed(
            title=get_localized_text("RU", "active_session"),
            description=get_localized_text("RU", "active_session_desc"),
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title=get_localized_text("RU", "welcome"),
        description=get_localized_text("RU", "greeting"),
        color=0x0099ff
    )
    
    view = create_language_view()
    
    try:
        # Пытаемся отправить в ЛС
        await user.send(embed=embed, view=view)
        success_embed = discord.Embed(
            title="✅ Успех",
            description=f"Верификация запущена в ЛС для пользователя {user.mention}",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=success_embed, ephemeral=True)
        
    except discord.Forbidden:
        # Если ЛС закрыты, запускаем верификацию в текущем канале
        warning_embed = discord.Embed(
            title="⚠️ Внимание",
            description=f"{user.mention} ЛС закрыты. Верификация запущена здесь.",
            color=0xffff00
        )
        await interaction.response.send_message(embed=warning_embed)
        
        # Отправляем основное сообщение верификации
        await interaction.channel.send(content=user.mention, embed=embed, view=view)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Ошибка",
            description=f"Не удалось запустить верификацию: {str(e)}",
            color=0xff0000
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)