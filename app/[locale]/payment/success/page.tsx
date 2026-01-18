import Link from 'next/link'

export default function PaymentSuccessPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto text-center">
        <div className="card">
          <div className="text-6xl mb-6">🎉</div>
          <h1 className="text-4xl font-bold mb-4">Оплата успішна!</h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
            Вітаємо! Ви успішно придбали курс. Тепер у вас є повний доступ до всіх уроків.
          </p>
          <div className="space-y-4">
            <Link href="/lessons" className="btn-primary inline-block">
              Почати навчання
            </Link>
            <Link
              href="/dashboard"
              className="btn-secondary inline-block ml-4"
            >
              Перейти в кабінет
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
