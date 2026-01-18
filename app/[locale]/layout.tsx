import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { notFound } from 'next/navigation'
import Header from '@/components/layout/Header'
import SessionProvider from '@/components/providers/SessionProvider'
import '../globals.css'

const locales = ['en', 'ru', 'uk']

export const metadata = {
  title: 'AI Learning Portal - Навчання роботі з ШІ',
  description: 'Практичний курс для освоєння ChatGPT, Claude та Perplexity',
}

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  if (!locales.includes(locale as any)) notFound()

  const messages = await getMessages()

  return (
    <html lang={locale} suppressHydrationWarning>
      <body className="min-h-screen">
        <SessionProvider>
          <NextIntlClientProvider messages={messages}>
            <Header />
            <main className="min-h-[calc(100vh-80px)]">
              {children}
            </main>
          </NextIntlClientProvider>
        </SessionProvider>
      </body>
    </html>
  )
}
