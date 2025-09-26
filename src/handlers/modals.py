import discord
import asyncio
import random
from discord.ui import Modal, TextInput, Button, View
from locales.locales import get_localized_text
from utils.storage import save_user_record
from config import settings

class VerificationModal(Modal):
    def __init__(self, lang: str):
        self.lang = lang
        super().__init__(title=get_localized_text(lang, "modal_title"))
        
        self.country = TextInput(
            label=get_localized_text(lang, "country_label"),
            placeholder=get_localized_text(lang, "country_placeholder"),
            required=True,
            max_length=50
        )
        
        self.nick = TextInput(
            label=get_localized_text(lang, "nick_label"),
            placeholder=get_localized_text(lang, "nick_placeholder"),
            required=True,
            max_length=50
        )
        
        self.level = TextInput(
            label=get_localized_text(lang, "level_label"),
            placeholder=get_localized_text(lang, "level_placeholder"),
            required=True,
            max_length=5
        )
        
        self.add_item(self.country)
        self.add_item(self.nick)
        self.add_item(self.level)

    async def on_submit(self, interaction: discord.Interaction):
        from handlers.sessions import user_sessions
        
        user_id = interaction.user.id
        answers = {
            "country": self.country.value,
            "nick": self.nick.value,
            "level": self.level.value
        }

        record = {
            "user_id": user_id,
            "username": str(interaction.user),
            "language": self.lang,
            "answers": answers,
        }
        
        save_user_record(record, settings.RESULTS_FILE)

        # Отправляем начальное сообщение о начале верификации
        initial_embed = discord.Embed(
            title=get_localized_text(self.lang, "verification_start"),
            description=get_localized_text(self.lang, "verification_processing"),
            color=0xFFFF00  # Желтый цвет для процесса
        )
        
        await interaction.response.send_message(embed=initial_embed, ephemeral=True)
        message = await interaction.original_response()
        
        # Запускаем асинхронную задачу для имитации задержки верификации
        asyncio.create_task(
            self.delayed_verification(interaction, message, self.lang, user_id)
        )

    async def delayed_verification(self, interaction: discord.Interaction, message: discord.Message, lang: str, user_id: int):
        """Имитация процесса верификации с визуальным прогресс-баром"""
        
        delay = random.randint(settings.MIN_DELAY_VERIFICATION, settings.MAX_DELAY_VERIFICATION)
        
        for progress in range(0, delay + 1):
            percentage = (progress / delay) * 100
            progress_bar = self.create_progress_bar(percentage, 20)
            
            processing_embed = discord.Embed(
                title=get_localized_text(lang, "verification_processing"),
                description=f"{progress_bar}\n\n{get_localized_text(lang, 'verification_delay').format(delay=delay-progress)}",
                color=0xFFFF00
            )
            
            try:
                await message.edit(embed=processing_embed)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error updating message: {e}")
                break
        
        # Финальное сообщение
        success_embed = discord.Embed(
            title=get_localized_text(lang, "verification_success"),
            description=get_localized_text(lang, "verify_label"),
            color=0x00FF00
        )
        
        button = Button(
            label=get_localized_text(lang, "verify_btn"),
            url=settings.VERIFY_URL,
            style=discord.ButtonStyle.link
        )
        
        view = View()
        view.add_item(button)

        try:
            await message.edit(embed=success_embed, view=view)
        except Exception as e:
            print(f"Error sending final message: {e}")
            try:
                await interaction.followup.send(embed=success_embed, view=view, ephemeral=True)
            except Exception as e2:
                print(f"Error sending followup: {e2}")
        
        # Очищаем сессию
        from handlers.sessions import user_sessions
        if user_id in user_sessions:
            del user_sessions[user_id]

    def create_progress_bar(self, percentage: float, length: int = 20) -> str:
        """Создает текстовый прогресс-бар"""
        filled_length = int(length * percentage / 100)
        bar = "█" * filled_length + "░" * (length - filled_length)
        return f"`[{bar}] {percentage:.1f}%`"