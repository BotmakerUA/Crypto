'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import ReactPlayer from 'react-player'

interface LessonViewerProps {
  lesson: {
    id: string
    title: string
    content: any
    order: number
  }
  progress: any
  nextLesson: any
  previousLesson: any
  userId: string
}

export default function LessonViewer({
  lesson,
  progress,
  nextLesson,
  previousLesson,
  userId,
}: LessonViewerProps) {
  const router = useRouter()
  const [isCompleting, setIsCompleting] = useState(false)

  const handleComplete = async () => {
    if (progress.status === 'COMPLETED') return

    setIsCompleting(true)
    try {
      const res = await fetch('/api/lessons/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lessonId: lesson.id }),
      })

      if (res.ok) {
        router.refresh()
        if (nextLesson) {
          router.push(`/lessons/${nextLesson.id}`)
        } else {
          router.push('/dashboard')
        }
      }
    } catch (error) {
      console.error('Error completing lesson:', error)
    } finally {
      setIsCompleting(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-4">
          Урок {lesson.order}: {lesson.title}
        </h1>
        {progress.status === 'COMPLETED' && (
          <div className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-4 py-2 rounded-lg inline-block">
            ✅ Завершено
          </div>
        )}
      </div>

      {/* Video */}
      {lesson.content?.videoUrl && (
        <div className="mb-8">
          <ReactPlayer
            url={lesson.content.videoUrl}
            controls
            width="100%"
            height="500px"
            className="rounded-lg overflow-hidden"
          />
        </div>
      )}

      {/* Text Content */}
      {lesson.content?.text && (
        <div
          className="prose dark:prose-invert max-w-none mb-8"
          dangerouslySetInnerHTML={{ __html: lesson.content.text }}
        />
      )}

      {/* Images */}
      {lesson.content?.images && lesson.content.images.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {lesson.content.images.map((img: string, index: number) => (
            <img
              key={index}
              src={img}
              alt={`Lesson image ${index + 1}`}
              className="rounded-lg w-full"
            />
          ))}
        </div>
      )}

      {/* Navigation */}
      <div className="flex items-center justify-between mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
        {previousLesson ? (
          <button
            onClick={() => router.push(`/lessons/${previousLesson.id}`)}
            className="btn-secondary"
          >
            ← Попередній урок
          </button>
        ) : (
          <div></div>
        )}

        {progress.status !== 'COMPLETED' && (
          <button
            onClick={handleComplete}
            disabled={isCompleting}
            className="btn-primary disabled:opacity-50"
          >
            {isCompleting ? 'Збереження...' : 'Завершити урок'}
          </button>
        )}

        {nextLesson && progress.status === 'COMPLETED' && (
          <button
            onClick={() => router.push(`/lessons/${nextLesson.id}`)}
            className="btn-primary"
          >
            Наступний урок →
          </button>
        )}
      </div>
    </div>
  )
}
