'use client'

import { useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'

export default function PaymentPage() {
  const t = useTranslations()
  const router = useRouter()
  const { data: session } = useSession()
  const [loading, setLoading] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState<'month' | 'lifetime'>('month')

  const prices = {
    month: 2900, // $29.00
    lifetime: 4900, // $49.00
  }

  const handleCheckout = async () => {
    if (!session?.user) {
      router.push('/auth/signin')
      return
    }

    setLoading(true)

    try {
      const res = await fetch('/api/stripe/create-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: selectedPlan,
          amount: prices[selectedPlan],
        }),
      })

      const { url } = await res.json()

      if (url) {
        window.location.href = url
      }
    } catch (error) {
      console.error('Checkout error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-4">{t('payment.title')}</h1>
        <p className="text-center text-gray-600 dark:text-gray-400 mb-12">
          Виберіть план, який вам підходить
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Month Plan */}
          <div
            className={`card cursor-pointer transition-all ${
              selectedPlan === 'month'
                ? 'border-primary border-2 shadow-xl'
                : 'border-gray-200 dark:border-gray-700'
            }`}
            onClick={() => setSelectedPlan('month')}
          >
            <div className="text-center">
              <h3 className="text-2xl font-bold mb-4">{t('payment.monthAccess')}</h3>
              <div className="text-5xl font-bold text-primary mb-4">$29</div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Доступ на 30 днів до всіх матеріалів курсу
              </p>
              <ul className="text-left space-y-3 mb-6">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  12 інтерактивних уроків
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Відео, тексти та зображення
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Telegram підтримка
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Сертифікат після завершення
                </li>
              </ul>
            </div>
          </div>

          {/* Lifetime Plan */}
          <div
            className={`card cursor-pointer transition-all relative ${
              selectedPlan === 'lifetime'
                ? 'border-primary border-2 shadow-xl'
                : 'border-gray-200 dark:border-gray-700'
            }`}
            onClick={() => setSelectedPlan('lifetime')}
          >
            <div className="absolute top-4 right-4 bg-primary text-white text-xs px-3 py-1 rounded-full">
              Краща ціна
            </div>
            <div className="text-center">
              <h3 className="text-2xl font-bold mb-4">{t('payment.lifetimeAccess')}</h3>
              <div className="text-5xl font-bold text-primary mb-4">$49</div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Безлімітний доступ до всіх матеріалів
              </p>
              <ul className="text-left space-y-3 mb-6">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Все з місячного плану
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  ♾️ Безлімітний доступ
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Всі майбутні оновлення
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Пріоритетна підтримка
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <button
            onClick={handleCheckout}
            disabled={loading}
            className="btn-primary text-lg px-12 py-4 disabled:opacity-50"
          >
            {loading ? t('common.loading') : t('payment.payNow')}
          </button>
          <p className="text-sm text-gray-500 mt-4">
            🔒 Безпечна оплата через Stripe
          </p>
        </div>
      </div>
    </div>
  )
}
