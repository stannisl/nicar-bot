# 🚀 Discord Bot (Python + discord.py)

Этот проект — Discord-бот, который ведёт диалог в ЛС:
- Выбор языка (RU / EN)
- Вопросы про Steam (страна, ник, уровень)
- Сохранение данных в JSON
- Ссылка на верификацию

---

## 🔧 Подготовка окружения

Перед запуском создайте файл `.env`:

```env
DISCORD_BOT_TOKEN=ваш_токен_бота
VERIFY_URL=https://example.com/verify
```

---

## 🐳 Запуск в Docker

### 1. Собрать образ

```bash
docker build -t discord-steam-bot .
```

### 2. Запустить контейнер

```bash
docker run -d \
  --name discord-steam-bot \
  --env-file .env \
  discord-steam-bot
```

---

## 🛠 Локальный запуск (без Docker)

1. Установите зависимости:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Создайте `.env` (см. выше).

3. Запустите:

   ```bash
   python bot.py
   ```

---

## 📂 Структура проекта

```
.
├── bot.py                 # Точка входа
├── handlers/              # Хендлеры (команды, модальные окна)
├── locales/               # Локализация (RU/EN)
├── utils/                 # Утилиты (хранение, логирование)
├── config.py              # Конфигурация
├── requirements.txt       # Python-зависимости
├── Dockerfile             # Docker образ
├── .env.example           # Пример конфигурации
└── README.md              # Документация
```

---

## ⚠️ Замечания

* Логи контейнера можно смотреть так:

  ```bash
  docker logs -f discord-steam-bot
  ```

* Чтобы обновить бота:

  ```bash
  docker stop discord-steam-bot && docker rm discord-steam-bot
  docker build -t discord-steam-bot .
  docker run -d --env-file .env discord-steam-bot
  ```

* Чтобы посмотреть файл `data.json` с ответами пользователей:

  1. Войти в работающий контейнер:

     ```bash
     docker exec -it discord-steam-bot /bin/sh
     ```
  2. Перейти в рабочую директорию:

     ```sh
     cd /app
     ```
  3. Просмотреть содержимое файла:

     ```sh
     cat data.json
     ```

Если нужно, можно сделать **монтирование файла наружу**, чтобы не заходить в контейнер:

```bash
docker run -d --env-file .env -v $(pwd)/data.json:/app/data.json discord-steam-bot
```

---

## 🔗 Создание бота и приглашение на сервер

1. Создайте приложение и бота на [Discord Developer Portal](https://discord.com/developers/applications)
2. В настройках бота включите **SERVER MEMBERS INTENT** и **MESSAGE CONTENT INTENT**
3. Сгенерируйте ссылку-приглашение с правами:
   - `applications.commands`
   - `bot`
   - Разрешения: `Send Messages`, `Read Message History`, `Use Slash Commands`

---

## 💬 Использование бота

Бот работает через слеш-команды:
- `/verify` - начать процесс верификации
- `/help` - показать справку
