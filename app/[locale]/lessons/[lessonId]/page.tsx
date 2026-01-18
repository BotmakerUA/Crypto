import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import { getLocale } from 'next-intl/server'
import { getLocalizedContent } from '@/lib/utils'
import LessonViewer from '@/components/lessons/LessonViewer'

export default async function LessonPage({ params }: { params: { lessonId: string } }) {
  const session = await getServerSession(authOptions)
  const locale = await getLocale()

  if (!session?.user) {
    redirect('/auth/signin')
  }

  const lesson = await prisma.lesson.findUnique({
    where: { id: params.lessonId },
    include: { course: true },
  })

  if (!lesson) {
    return <div>Урок не знайдено</div>
  }

  // Check access
  const subscription = await prisma.subscription.findFirst({
    where: {
      userId: session.user.id,
      courseId: lesson.courseId,
      status: 'ACTIVE',
    },
  })

  if (!lesson.isFree && !subscription) {
    redirect('/lessons')
  }

  // Get or create progress
  let progress = await prisma.progress.findUnique({
    where: {
      userId_lessonId: {
        userId: session.user.id,
        lessonId: lesson.id,
      },
    },
  })

  if (!progress) {
    progress = await prisma.progress.create({
      data: {
        userId: session.user.id,
        lessonId: lesson.id,
        status: 'IN_PROGRESS',
      },
    })
  } else if (progress.status === 'NOT_STARTED') {
    progress = await prisma.progress.update({
      where: { id: progress.id },
      data: { status: 'IN_PROGRESS' },
    })
  }

  // Get next and previous lessons
  const nextLesson = await prisma.lesson.findFirst({
    where: {
      courseId: lesson.courseId,
      order: { gt: lesson.order },
    },
    orderBy: { order: 'asc' },
  })

  const previousLesson = await prisma.lesson.findFirst({
    where: {
      courseId: lesson.courseId,
      order: { lt: lesson.order },
    },
    orderBy: { order: 'desc' },
  })

  const title = getLocalizedContent(lesson.title, locale)
  const content = getLocalizedContent(lesson.content, locale)

  return (
    <LessonViewer
      lesson={{
        id: lesson.id,
        title,
        content,
        order: lesson.order,
      }}
      progress={progress}
      nextLesson={nextLesson}
      previousLesson={previousLesson}
      userId={session.user.id}
    />
  )
}
