import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import { getTranslations } from 'next-intl/server'
import LessonCard from '@/components/lessons/LessonCard'

export default async function LessonsPage() {
  const session = await getServerSession(authOptions)
  const t = await getTranslations()

  if (!session?.user) {
    redirect('/auth/signin')
  }

  // Get course
  const course = await prisma.course.findFirst({
    where: { isPublished: true },
    include: {
      lessons: {
        orderBy: { order: 'asc' },
      },
    },
  })

  if (!course) {
    return (
      <div className="container mx-auto px-4 py-12">
        <p>Курс ще не опубліковано</p>
      </div>
    )
  }

  // Get user subscription
  const subscription = await prisma.subscription.findFirst({
    where: {
      userId: session.user.id,
      courseId: course.id,
      status: 'ACTIVE',
    },
  })

  // Get user progress
  const progress = await prisma.progress.findMany({
    where: {
      userId: session.user.id,
      lessonId: { in: course.lessons.map((l) => l.id) },
    },
  })

  const progressMap = new Map(progress.map((p) => [p.lessonId, p]))

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">{t('lessons.title')}</h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {course.lessons.map((lesson, index) => {
          const lessonProgress = progressMap.get(lesson.id)
          const isLocked = !lesson.isFree && !subscription && index > 0
          const previousLesson = index > 0 ? course.lessons[index - 1] : null
          const previousCompleted = previousLesson
            ? progressMap.get(previousLesson.id)?.status === 'COMPLETED'
            : true

          return (
            <LessonCard
              key={lesson.id}
              lesson={lesson}
              progress={lessonProgress}
              isLocked={isLocked || !previousCompleted}
              courseId={course.id}
            />
          )
        })}
      </div>

      {!subscription && (
        <div className="mt-12 card bg-primary-light bg-opacity-10 border-primary">
          <h2 className="text-2xl font-bold mb-4">Отримайте повний доступ</h2>
          <p className="mb-6">
            Перший урок безкоштовний! Щоб продовжити навчання, придбайте повний доступ до курсу.
          </p>
          <a
            href="/payment"
            className="btn-primary inline-block"
          >
            Придбати курс
          </a>
        </div>
      )}
    </div>
  )
}
