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

        # Создаем кнопку для верификации
        button = Button(
            label=get_localized_text(self.lang, "verify_btn"),
            url=settings.VERIFY_URL,
            style=discord.ButtonStyle.link
        )
        
        view = View()
        view.add_item(button)

        # Отправляем сообщение с кнопкой верификации
        verify_embed = discord.Embed(
            title=get_localized_text(self.lang, "verification_start"),
            description=get_localized_text(self.lang, "verify_label"),
            color=0x0099ff
        )
        
        await interaction.response.send_message(embed=verify_embed, view=view, ephemeral=True)
        message = await interaction.original_response()
        
        # Запускаем асинхронную задачу для задержки и завершения верификации
        asyncio.create_task(
            self.delayed_verification_completion(interaction, message, self.lang, user_id)
        )

    async def delayed_verification_completion(self, interaction: discord.Interaction, message: discord.Message, lang: str, user_id: int):
        """Завершение верификации после задержки"""
        
        # Случайная задержка
        delay = random.randint(settings.MIN_DELAY_VERIFICATION, settings.MAX_DELAY_VERIFICATION)
        
        # Ждем указанное время
        await asyncio.sleep(delay)
        
        # Создаем embed для завершения верификации
        success_embed = discord.Embed(
            title=get_localized_text(lang, "verification_success"),
            description="✅ Ваши данные были успешно обработаны и подтверждены!",
            color=0x00ff00
        )
        
        try:
            # Редактируем исходное сообщение
            await message.edit(embed=success_embed, view=None)
        except Exception as e:
            print(f"Error editing message: {e}")
            try:
                # Если не удалось редактировать, отправляем новое сообщение
                await interaction.followup.send(embed=success_embed, ephemeral=True)
            except Exception as e2:
                print(f"Error sending followup: {e2}")
        
        # Очищаем сессию
        from handlers.sessions import user_sessions
        if user_id in user_sessions:
            del user_sessions[user_id]