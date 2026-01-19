# AI Learning Portal

Платформа для навчання використанню ШІ (ChatGPT, Claude, Perplexity) в повсякденному житті.

## Особливості

- 🌍 **Мультимовність**: Українська, російська та англійська мови
- 🎨 **Теми**: Світла та темна теми
- 📚 **12 уроків**: Структурований курс на місяць
- 💳 **Платежі**: Інтеграція зі Stripe
- 📱 **Telegram**: Нагадування та повідомлення
- 🔐 **Авторизація**: Email або телефон
- 📊 **Прогрес**: Відстеження виконання уроків
- 👑 **Адмін-панель**: Управління курсом та користувачами

## Технології

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, PostgreSQL, Prisma
- **Аутентифікація**: NextAuth.js
- **Платежі**: Stripe
- **Повідомлення**: Telegram Bot API
- **Інтернаціоналізація**: next-intl
- **Стан**: Zustand

## Встановлення

1. Клонуйте репозиторій
2. Встановіть залежності:
```bash
npm install
```

3. Створіть файл `.env`:
```bash
cp .env.example .env
```

4. Налаштуйте змінні оточення в `.env`:
- `DATABASE_URL` - URL PostgreSQL бази даних
- `NEXTAUTH_SECRET` - секретний ключ для NextAuth
- `STRIPE_SECRET_KEY` - секретний ключ Stripe
- `STRIPE_PUBLISHABLE_KEY` - публічний ключ Stripe
- `STRIPE_WEBHOOK_SECRET` - секрет для вебхуків Stripe
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота

5. Запустіть міграції Prisma:
```bash
npx prisma migrate dev
npx prisma generate
```

6. Створіть первинні дані (опціонально):
```bash
npm run seed
```

7. Запустіть проєкт:
```bash
npm run dev
```

Проєкт буде доступний на `http://localhost:3000`

## Структура проєкту

```
├── app/                    # Next.js App Router
│   ├── [locale]/          # Локалізовані сторінки
│   │   ├── page.tsx       # Головна сторінка
│   │   ├── auth/          # Авторизація
│   │   ├── lessons/       # Уроки
│   │   ├── dashboard/     # Кабінет користувача
│   │   ├── payment/       # Оплата
│   │   └── admin/         # Адмін-панель
│   └── api/               # API routes
├── components/            # React компоненти
│   ├── layout/           # Компоненти лейауту
│   ├── ui/               # UI компоненти
│   └── lessons/          # Компоненти уроків
├── lib/                  # Утиліти та конфігурація
│   ├── auth/            # Налаштування NextAuth
│   ├── db.ts            # Prisma клієнт
│   ├── stripe/          # Stripe інтеграція
│   └── telegram/        # Telegram Bot
├── prisma/              # Prisma схеми та міграції
├── messages/            # Переклади
└── public/              # Статичні файли
```

## Основні функції

### Для користувачів

- Реєстрація через email або телефон
- Безкоштовний доступ до першого уроку
- Покупка курсу (місячний або безлімітний доступ)
- Проходження уроків з текстом, зображеннями та відео
- Відстеження прогресу
- Telegram нагадування про наступні уроки
- Переключення мови інтерфейсу
- Світла та темна теми

### Для адміністраторів

- Управління уроками (створення, редагування)
- Перегляд користувачів та підписок
- Статистика та аналітика
- Управління контентом на трьох мовах

## Налаштування Stripe

1. Створіть обліковий запис на [Stripe](https://stripe.com)
2. Отримайте API ключі в Dashboard
3. Налаштуйте webhook endpoint: `https://your-domain.com/api/stripe/webhook`
4. Додайте події: `checkout.session.completed`

## Налаштування Telegram Bot

1. Створіть бота через [@BotFather](https://t.me/botfather)
2. Отримайте токен бота
3. Додайте токен у `.env`
4. Користувачі зможуть підключити свій Telegram для отримання повідомлень

## Deployment

### 🚀 Быстрый деплой на Vercel (1 минута)

**Шаг 1:** Перейдите на [Vercel](https://vercel.com) и войдите через GitHub

**Шаг 2:** Нажмите "Add New Project" → Import Git Repository → выберите этот репозиторий

**Шаг 3:** Добавьте бесплатную базу данных PostgreSQL:
- Перейдите в Storage → Create Database → Postgres
- Или подключите [Neon](https://neon.tech) (бесплатно 0.5GB)

**Шаг 4:** Добавьте минимальные переменные окружения:
```
DATABASE_URL=ваш-postgres-url
NEXTAUTH_URL=https://ваш-проект.vercel.app
NEXTAUTH_SECRET=любая-секретная-строка
```

**Шаг 5:** Нажмите Deploy! 🎉

Ваш сайт будет доступен по адресу `https://ваш-проект.vercel.app`

---

### Альтернативные варианты

Проєкт также можно развернуть на:
- Railway
- Render
- DigitalOcean
- AWS

Не забудьте налаштувати:
- PostgreSQL базу даних
- Змінні оточення
- Stripe webhook endpoint
- Domain для NEXTAUTH_URL

## Ліцензія

MIT
