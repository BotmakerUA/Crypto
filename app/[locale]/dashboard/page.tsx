import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import { getTranslations } from 'next-intl/server'
import Link from 'next/link'

export default async function DashboardPage() {
  const session = await getServerSession(authOptions)
  const t = await getTranslations()

  if (!session?.user) {
    redirect('/auth/signin')
  }

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    include: {
      subscriptions: {
        where: { status: 'ACTIVE' },
        include: { course: true },
      },
      progress: {
        where: { status: 'COMPLETED' },
      },
    },
  })

  const activeSubscription = user?.subscriptions[0]
  const completedLessons = user?.progress.length || 0

  const totalLessons = activeSubscription
    ? await prisma.lesson.count({
        where: { courseId: activeSubscription.courseId },
      })
    : 12 // default

  const progressPercentage = (completedLessons / totalLessons) * 100

  const daysLeft = activeSubscription
    ? Math.ceil(
        (new Date(activeSubscription.endDate).getTime() - Date.now()) /
          (1000 * 60 * 60 * 24)
      )
    : 0

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">{t('dashboard.title')}</h1>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        {/* Progress Card */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">{t('dashboard.myProgress')}</h3>
          <div className="text-4xl font-bold text-primary mb-2">
            {Math.round(progressPercentage)}%
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progressPercentage}%` }} />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            {completedLessons} з {totalLessons} уроків
          </p>
        </div>

        {/* Time Left Card */}
        {activeSubscription && !activeSubscription.isLifetime && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">{t('dashboard.timeLeft')}</h3>
            <div className="text-4xl font-bold text-primary mb-2">
              {daysLeft > 0 ? daysLeft : 0}
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">днів</p>
          </div>
        )}

        {activeSubscription?.isLifetime && (
          <div className="card bg-green-50 dark:bg-green-900">
            <h3 className="text-lg font-semibold mb-4">Доступ</h3>
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              ♾️ Безлімітний
            </div>
          </div>
        )}

        {/* Completed Lessons Card */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">{t('dashboard.completedLessons')}</h3>
          <div className="text-4xl font-bold text-primary mb-2">
            {completedLessons}
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">уроків завершено</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <Link href="/lessons" className="card hover:shadow-xl transition-shadow">
          <h3 className="text-2xl font-bold mb-2">📚 Продовжити навчання</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Перейдіть до уроків і продовжте своє навчання
          </p>
        </Link>

        {activeSubscription && daysLeft < 7 && !activeSubscription.isLifetime && (
          <Link href="/payment/extend" className="card bg-primary-light bg-opacity-10 border-primary hover:shadow-xl transition-shadow">
            <h3 className="text-2xl font-bold mb-2">⏰ {t('dashboard.extendAccess')}</h3>
            <p className="text-gray-600 dark:text-gray-400">
              У вас залишилось {daysLeft} днів. Продовжте доступ до курсу!
            </p>
          </Link>
        )}

        {!activeSubscription && (
          <Link href="/payment" className="card bg-primary-light bg-opacity-10 border-primary hover:shadow-xl transition-shadow">
            <h3 className="text-2xl font-bold mb-2">💳 Придбати курс</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Отримайте повний доступ до всіх уроків курсу
            </p>
          </Link>
        )}
      </div>
    </div>
  )
}
