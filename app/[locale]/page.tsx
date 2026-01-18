import { useTranslations } from 'next-intl'
import Link from 'next/link'
import { getTranslations } from 'next-intl/server'

export default async function HomePage() {
  const t = await getTranslations()

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-light via-white to-primary-light dark:from-gray-800 dark:via-gray-900 dark:to-gray-800 py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-gray-900 dark:text-white">
            {t('home.hero.title')}
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-700 dark:text-gray-300 max-w-3xl mx-auto">
            {t('home.hero.subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/auth/signup" className="btn-primary text-lg px-8 py-4">
              {t('home.hero.cta')}
            </Link>
            <p className="text-primary font-semibold">
              ✨ {t('home.hero.freeTrial')}
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
            {t('home.features.title')}
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="text-5xl mb-4">💡</div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">
                {t('home.features.practical.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {t('home.features.practical.description')}
              </p>
            </div>
            <div className="card text-center">
              <div className="text-5xl mb-4">📚</div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">
                {t('home.features.stepByStep.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {t('home.features.stepByStep.description')}
              </p>
            </div>
            <div className="card text-center">
              <div className="text-5xl mb-4">🔔</div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">
                {t('home.features.support.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {t('home.features.support.description')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Course Structure */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
            Структура курсу
          </h2>
          <div className="max-w-4xl mx-auto">
            <div className="space-y-6">
              {[
                { week: 1, lessons: 'Уроки 1-3: Основи роботи з ChatGPT' },
                { week: 2, lessons: 'Уроки 4-6: Практичне використання ChatGPT' },
                { week: 3, lessons: 'Уроки 7-9: Знайомство з Claude та Perplexity' },
                { week: 4, lessons: 'Уроки 10-12: Комплексне використання ШІ' },
              ].map((item) => (
                <div key={item.week} className="card flex items-center gap-4">
                  <div className="text-3xl font-bold text-primary w-16 h-16 flex items-center justify-center bg-primary-light bg-opacity-20 rounded-full">
                    {item.week}
                  </div>
                  <div className="flex-1">
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {item.lessons}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Готові розпочати навчання?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Приєднуйтесь до курсу та вже через місяць ви зможете впевнено використовувати ШІ у своєму житті
          </p>
          <Link
            href="/auth/signup"
            className="inline-block px-8 py-4 bg-white text-primary rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors"
          >
            Почати зараз
          </Link>
        </div>
      </section>
    </div>
  )
}
