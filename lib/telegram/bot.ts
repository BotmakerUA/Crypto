import TelegramBot from 'node-telegram-bot-api'

let bot: TelegramBot | null = null

export function getTelegramBot() {
  if (!process.env.TELEGRAM_BOT_TOKEN) {
    console.warn('TELEGRAM_BOT_TOKEN is not set')
    return null
  }

  if (!bot) {
    bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: false })
  }

  return bot
}

export async function sendTelegramNotification(
  telegramId: string,
  message: string
) {
  const bot = getTelegramBot()
  if (!bot) return

  try {
    await bot.sendMessage(telegramId, message, { parse_mode: 'HTML' })
  } catch (error) {
    console.error('Failed to send telegram notification:', error)
  }
}

export async function sendLessonReminder(
  telegramId: string,
  lessonTitle: string,
  locale: string = 'uk'
) {
  const messages = {
    uk: `🔔 Нагадування: наступний урок "${lessonTitle}" вже доступний!`,
    ru: `🔔 Напоминание: следующий урок "${lessonTitle}" уже доступен!`,
    en: `🔔 Reminder: next lesson "${lessonTitle}" is now available!`,
  }

  const message = messages[locale as keyof typeof messages] || messages.uk
  await sendTelegramNotification(telegramId, message)
}
