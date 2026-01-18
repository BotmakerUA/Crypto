'use client'

import { useLocale } from 'next-intl'
import Link from 'next/link'
import { getLocalizedContent } from '@/lib/utils'

interface LessonCardProps {
  lesson: any
  progress: any
  isLocked: boolean
  courseId: string
}

export default function LessonCard({ lesson, progress, isLocked, courseId }: LessonCardProps) {
  const locale = useLocale()
  const title = getLocalizedContent(lesson.title, locale)
  const description = getLocalizedContent(lesson.description, locale)

  const getStatusIcon = () => {
    if (isLocked) return '🔒'
    if (progress?.status === 'COMPLETED') return '✅'
    if (progress?.status === 'IN_PROGRESS') return '▶️'
    return '⭕'
  }

  const getStatusText = () => {
    if (isLocked) return 'Заблоковано'
    if (progress?.status === 'COMPLETED') return 'Завершено'
    if (progress?.status === 'IN_PROGRESS') return 'В процесі'
    return 'Не розпочато'
  }

  return (
    <div className={`lesson-card ${isLocked ? 'opacity-60' : ''}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="text-3xl">{getStatusIcon()}</div>
        {lesson.isFree && (
          <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
            Безкоштовно
          </span>
        )}
      </div>

      <h3 className="text-xl font-bold mb-2">
        Урок {lesson.order}: {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-4">{description}</p>

      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-500">{getStatusText()}</span>
        {!isLocked && (
          <Link
            href={`/lessons/${lesson.id}`}
            className="btn-primary text-sm px-4 py-2"
          >
            {progress?.status === 'COMPLETED' ? 'Переглянути' : 'Почати'}
          </Link>
        )}
      </div>
    </div>
  )
}
