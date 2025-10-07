LOCALES = {
    "RU": {
        # Общие
        "greeting": "👋 Hello! Let's get started. Please choose your language 🌐",
        "choose_lang": "Выберите язык / Choose language",
        "cancel": "❌ Отмена",
        "verify_label": "✅ Пожалуйста, продолжи верификацию на сайте:",
        
        # Ошибки
        "active_session": "❌ У вас уже есть активная сессия",
        "active_session_desc": "Завершите текущую верификацию или используйте /cancel",
        "no_session": "❌ Нет активной сессии",
        "no_session_desc": "У вас нет активной верификации для отмены.",
        
        # Вопросы
        "ask_country": "Из какой ты страны? 🌍",
        "ask_nick": "Какой у тебя никнейм в Steam? 🎮", 
        "ask_level": "Какой у тебя уровень в Steam? ⭐",
        
        # Кнопки и селекты
        "btn_ru": "🇷🇺 Русский",
        "btn_en": "🇬🇧 English",
        "select_placeholder": "Выберите язык / Choose language...",
        "ru_option": "Русский",
        "en_option": "English",
        "ru_desc": "Выбрать русский язык",
        "en_desc": "Choose English language",
        
        # Заголовки
        "welcome": "👋 Welcome!",
        "help_title": "📖 Справка по командам",
        "help_desc": "Доступные команды бота:",
        "verify_complete": "✅ Верификация завершена!",
        
        # Модальное окно
        "modal_title": "Steam Verification",
        "country_label": "Ваша страна",
        "country_placeholder": "Введите страну",
        "nick_label": "Ваш Steam никнейм", 
        "nick_placeholder": "Введите никнейм",
        "level_label": "Ваш Steam уровень",
        "level_placeholder": "Введите уровень",
        "verify_btn": "✅ Перейти к верификации",

        "verification_start": "🔍 Начинаем верификацию...",
        "verification_processing": "⏳ Проверяем ваши данные...",
        "verification_delay": "Пожалуйста, подождите {delay} секунд",
        "verification_success": "✅ Верификация успешно завершена!",
        "verification_complete": "✅ Верификация завершена!",
    },
    "EN": {
        # General
        "verification_complete": "✅ Verification complete!",
        "greeting": "👋 Hello! Let's get started. Please choose your language 🌐",
        "choose_lang": "Choose your language:",
        "cancel": "❌ Cancel",
        "verify_label": "✅ Please continue verification on the website:",
        
        # Errors
        "active_session": "❌ You already have an active session",
        "active_session_desc": "Complete the current verification or use /cancel",
        "no_session": "❌ No active session", 
        "no_session_desc": "You don't have an active verification to cancel.",
        
        # Questions
        "ask_country": "Which country are you from? 🌍",
        "ask_nick": "What's your Steam nickname? 🎮",
        "ask_level": "What's your Steam level? ⭐",
        
        # Buttons and selects
        "btn_ru": "🇷🇺 Russian",
        "btn_en": "🇬🇧 English",
        "select_placeholder": "Choose language...",
        "ru_option": "Russian",
        "en_option": "English", 
        "ru_desc": "Choose Russian language",
        "en_desc": "Choose English language",
        
        # Titles
        "welcome": "👋 Welcome!",
        "help_title": "📖 Command help",
        "help_desc": "Available bot commands:",
        "verify_complete": "✅ Verification complete!",
        
        # Modal
        "modal_title": "Steam Verification",
        "country_label": "Your country",
        "country_placeholder": "Enter your country",
        "nick_label": "Your Steam nickname",
        "nick_placeholder": "Enter your nickname",
        "level_label": "Your Steam level",
        "level_placeholder": "Enter your level",
        "verify_btn": "✅ Go to verification",

        "verification_start": "🔍 Starting verification...",
        "verification_processing": "⏳ Checking your data...",
        "verification_delay": "Please wait {delay} seconds",
        "verification_success": "✅ Verification completed successfully!",
    }
}

def get_localized_text(lang: str, key: str) -> str:
    """Безопасное получение локализованного текста"""
    return LOCALES.get(lang, LOCALES["EN"]).get(key, key)