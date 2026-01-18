import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth/config'
import { prisma } from '@/lib/db'
import { sendLessonReminder } from '@/lib/telegram/bot'

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { lessonId } = await req.json()

    // Update progress
    const progress = await prisma.progress.update({
      where: {
        userId_lessonId: {
          userId: session.user.id,
          lessonId,
        },
      },
      data: {
        status: 'COMPLETED',
        completedAt: new Date(),
      },
    })

    // Get current lesson to find next lesson
    const currentLesson = await prisma.lesson.findUnique({
      where: { id: lessonId },
    })

    if (currentLesson) {
      const nextLesson = await prisma.lesson.findFirst({
        where: {
          courseId: currentLesson.courseId,
          order: { gt: currentLesson.order },
        },
        orderBy: { order: 'asc' },
      })

      // Send telegram notification about next lesson
      if (nextLesson) {
        const user = await prisma.user.findUnique({
          where: { id: session.user.id },
        })

        if (user?.telegramId) {
          const lessonTitle = nextLesson.title as any
          await sendLessonReminder(
            user.telegramId,
            lessonTitle.uk || lessonTitle.en || 'Next lesson',
            user.locale
          )
        }
      }
    }

    return NextResponse.json({ success: true, progress })
  } catch (error) {
    console.error('Complete lesson error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
