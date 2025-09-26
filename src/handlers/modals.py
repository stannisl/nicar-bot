import discord
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

        embed = discord.Embed(
            title=get_localized_text(self.lang, "verify_complete"),
            description=get_localized_text(self.lang, "verify_label"),
            color=0x00ff00
        )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        # Очищаем сессию
        if user_id in user_sessions:
            del user_sessions[user_id]