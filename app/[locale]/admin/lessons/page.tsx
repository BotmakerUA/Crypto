import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import Link from 'next/link'

export default async function AdminLessonsPage() {
  const session = await getServerSession(authOptions)

  if (!session?.user || session.user.role !== 'ADMIN') {
    redirect('/')
  }

  const course = await prisma.course.findFirst({
    include: {
      lessons: {
        orderBy: { order: 'asc' },
      },
    },
  })

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold">Управління уроками</h1>
        <Link href="/admin/lessons/create" className="btn-primary">
          + Створити урок
        </Link>
      </div>

      {course ? (
        <div className="space-y-4">
          {course.lessons.map((lesson) => (
            <div key={lesson.id} className="card flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold">
                  Урок {lesson.order}: {(lesson.title as any).uk || (lesson.title as any).en}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {lesson.isFree ? '🆓 Безкоштовний' : '🔒 Платний'} |{' '}
                  {lesson.isPublished ? '✅ Опубліковано' : '⏸️ Чернетка'}
                </p>
              </div>
              <div className="flex gap-2">
                <Link
                  href={`/admin/lessons/${lesson.id}/edit`}
                  className="btn-secondary"
                >
                  Редагувати
                </Link>
              </div>
            </div>
          ))}

          {course.lessons.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Уроки ще не створені
              </p>
              <Link href="/admin/lessons/create" className="btn-primary">
                Створити перший урок
              </Link>
            </div>
          )}
        </div>
      ) : (
        <div className="card text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">Курс ще не створено</p>
        </div>
      )}
    </div>
  )
}
