# 🚀 Telegram Bot (Python + PTB)

Этот проект — Telegram-бот, который ведёт диалог в ЛС:
- Выбор языка (RU / EN)
- Вопросы про Steam (страна, ник, уровень)
- Сохранение данных в JSON
- Ссылка на верификацию

---

## 🔧 Подготовка окружения

Перед запуском создайте файл `.env`:

```env
BOT_TOKEN=ваш_токен_бота
VERIFY_URL=https://example.com/verify
````

---

## 🐳 Запуск в Docker

### 1. Собрать образ

```bash
docker build -t steam-bot .
```

### 2. Запустить контейнер

```bash
docker run -d \
  --name steam-bot \
  --env-file .env \
  steam-bot
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
   python src/bot.py
   ```

---

## 📂 Структура проекта

```
.
├── src/
│   ├── bot.py             # Точка входа
│   ├── handlers/          # Хендлеры
│   ├── locales/           # Локализация (RU/EN)
│   └── config.json        # Конфиг файл
├── requirements.txt       # Python-зависимости
├── Dockerfile             # Docker образ
├── .env.example           # Пример конфигурации
└── README.md              # Документация
```

---

Добавим инструкцию по просмотру файла данных внутри контейнера:

---

## ⚠️ Замечания

* Логи контейнера можно смотреть так:

  ```bash
  docker logs -f steam-bot
  ```

* Чтобы обновить бота:

  ```bash
  docker stop steam-bot && docker rm steam-bot
  docker build -t steam-bot .
  docker run -d --env-file .env steam-bot
  ```

* Чтобы посмотреть файл `storage.json` (или `data.json`) с ответами пользователей:

  1. Войти в работающий контейнер:

     ```bash
     docker exec -it steam-bot /bin/sh
     ```
  2. Перейти в рабочую директорию:

     ```sh
     cd /app
     ```
  3. Просмотреть содержимое файла:

     ```sh
     cat storage.json
     ```

     или открыть с помощью `less`/`more`:

     ```sh
     less storage.json
     ```

Если нужно, можно сделать **монтирование файла наружу**, чтобы не заходить в контейнер:

```bash
docker run -d --env-file .env -v $(pwd)/storage.json:/app/storage.json steam-bot
```

Тогда изменения будут видны прямо на хосте.
