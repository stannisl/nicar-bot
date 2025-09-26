import discord
from discord.ui import View, Select
from locales.locales import get_localized_text

class LanguageSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=get_localized_text("RU", "ru_option"),
                value="RU", 
                emoji="🇷🇺",
                description=get_localized_text("RU", "ru_desc")
            ),
            discord.SelectOption(
                label=get_localized_text("EN", "en_option"),
                value="EN",
                emoji="🇬🇧", 
                description=get_localized_text("EN", "en_desc")
            ),
        ]
        super().__init__(
            placeholder=get_localized_text("EN", "select_placeholder"),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        from handlers.sessions import user_sessions
        from handlers.modals import VerificationModal
        
        user_id = interaction.user.id
        lang = self.values[0]
        user_sessions[user_id] = lang

        modal = VerificationModal(lang=lang)
        await interaction.response.send_modal(modal)

def create_language_view() -> View:
    """Создает View с селектом языка (вызывается только при команде)"""
    view = View(timeout=300)
    view.add_item(LanguageSelect())
    return view