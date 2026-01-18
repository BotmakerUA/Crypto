import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import Link from 'next/link'

export default async function AdminPage() {
  const session = await getServerSession(authOptions)

  if (!session?.user || session.user.role !== 'ADMIN') {
    redirect('/')
  }

  const stats = {
    totalUsers: await prisma.user.count(),
    activeSubscriptions: await prisma.subscription.count({
      where: { status: 'ACTIVE' },
    }),
    totalRevenue: await prisma.payment.aggregate({
      where: { status: 'SUCCEEDED' },
      _sum: { amount: true },
    }),
    totalLessons: await prisma.lesson.count(),
  }

  const recentUsers = await prisma.user.findMany({
    take: 10,
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      email: true,
      phone: true,
      createdAt: true,
    },
  })

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Адмін-панель</h1>

      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-6 mb-12">
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Користувачів</h3>
          <div className="text-4xl font-bold text-primary">{stats.totalUsers}</div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Активних підписок</h3>
          <div className="text-4xl font-bold text-primary">{stats.activeSubscriptions}</div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Дохід</h3>
          <div className="text-4xl font-bold text-primary">
            ${((stats.totalRevenue._sum.amount || 0) / 100).toFixed(0)}
          </div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Уроків</h3>
          <div className="text-4xl font-bold text-primary">{stats.totalLessons}</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <Link href="/admin/lessons" className="card hover:shadow-xl transition-shadow">
          <h3 className="text-xl font-bold mb-2">📚 Управління уроками</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Створення, редагування та видалення уроків
          </p>
        </Link>
        <Link href="/admin/users" className="card hover:shadow-xl transition-shadow">
          <h3 className="text-xl font-bold mb-2">👥 Користувачі</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Перегляд та управління користувачами
          </p>
        </Link>
        <Link href="/admin/analytics" className="card hover:shadow-xl transition-shadow">
          <h3 className="text-xl font-bold mb-2">📊 Аналітика</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Статистика та звіти
          </p>
        </Link>
      </div>

      {/* Recent Users */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Нові користувачі</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4">Email/Телефон</th>
                <th className="text-left py-3 px-4">Дата реєстрації</th>
              </tr>
            </thead>
            <tbody>
              {recentUsers.map((user) => (
                <tr key={user.id} className="border-b border-gray-100 dark:border-gray-800">
                  <td className="py-3 px-4">{user.email || user.phone}</td>
                  <td className="py-3 px-4">
                    {new Date(user.createdAt).toLocaleDateString('uk-UA')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
