import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 10)
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      passwordHash: adminPassword,
      role: 'ADMIN',
      name: 'Admin',
    },
  })

  console.log('Admin created:', admin.email)

  // Create course
  const course = await prisma.course.upsert({
    where: { slug: 'ai-essentials' },
    update: {},
    create: {
      slug: 'ai-essentials',
      title: {
        uk: 'Основи використання ШІ',
        ru: 'Основы использования ИИ',
        en: 'AI Essentials',
      },
      description: {
        uk: 'Навчіться використовувати ChatGPT, Claude та Perplexity у повсякденному житті',
        ru: 'Научитесь использовать ChatGPT, Claude и Perplexity в повседневной жизни',
        en: 'Learn to use ChatGPT, Claude, and Perplexity in everyday life',
      },
      isPublished: true,
      price: 2900, // $29.00
      durationDays: 30,
    },
  })

  console.log('Course created:', course.slug)

  // Create lessons
  const lessons = [
    {
      order: 1,
      title: {
        uk: 'Що таке штучний інтелект?',
        ru: 'Что такое искусственный интеллект?',
        en: 'What is Artificial Intelligence?',
      },
      description: {
        uk: 'Знайомство з основами ШІ та його можливостями',
        ru: 'Знакомство с основами ИИ и его возможностями',
        en: 'Introduction to AI basics and capabilities',
      },
      content: {
        uk: {
          text: '<h2>Вступ до ШІ</h2><p>У цьому уроці ви дізнаєтесь про основи штучного інтелекту...</p>',
          images: [],
          videoUrl: '',
        },
        ru: {
          text: '<h2>Введение в ИИ</h2><p>В этом уроке вы узнаете об основах искусственного интеллекта...</p>',
          images: [],
          videoUrl: '',
        },
        en: {
          text: '<h2>Introduction to AI</h2><p>In this lesson you will learn about the basics of artificial intelligence...</p>',
          images: [],
          videoUrl: '',
        },
      },
      isFree: true,
      isPublished: true,
    },
    {
      order: 2,
      title: {
        uk: 'Перше знайомство з ChatGPT',
        ru: 'Первое знакомство с ChatGPT',
        en: 'First Steps with ChatGPT',
      },
      description: {
        uk: 'Створення акаунту та перші кроки',
        ru: 'Создание аккаунта и первые шаги',
        en: 'Creating an account and first steps',
      },
      content: {
        uk: {
          text: '<h2>ChatGPT для початківців</h2><p>Давайте розпочнемо роботу з ChatGPT...</p>',
          images: [],
          videoUrl: '',
        },
        ru: {
          text: '<h2>ChatGPT для начинающих</h2><p>Давайте начнем работу с ChatGPT...</p>',
          images: [],
          videoUrl: '',
        },
        en: {
          text: '<h2>ChatGPT for Beginners</h2><p>Let\'s get started with ChatGPT...</p>',
          images: [],
          videoUrl: '',
        },
      },
      isFree: false,
      isPublished: true,
    },
    {
      order: 3,
      title: {
        uk: 'Як правильно формулювати запити',
        ru: 'Как правильно формулировать запросы',
        en: 'How to Write Effective Prompts',
      },
      description: {
        uk: 'Техніки написання ефективних промптів',
        ru: 'Техники написания эффективных промптов',
        en: 'Techniques for writing effective prompts',
      },
      content: {
        uk: {
          text: '<h2>Майстерність промптів</h2><p>Навчіться створювати запити, які дають найкращі результати...</p>',
          images: [],
          videoUrl: '',
        },
        ru: {
          text: '<h2>Мастерство промптов</h2><p>Научитесь создавать запросы, которые дают лучшие результаты...</p>',
          images: [],
          videoUrl: '',
        },
        en: {
          text: '<h2>Prompt Mastery</h2><p>Learn to create prompts that give the best results...</p>',
          images: [],
          videoUrl: '',
        },
      },
      isFree: false,
      isPublished: true,
    },
  ]

  for (const lessonData of lessons) {
    await prisma.lesson.upsert({
      where: {
        courseId_order: {
          courseId: course.id,
          order: lessonData.order,
        },
      },
      update: {},
      create: {
        ...lessonData,
        courseId: course.id,
      },
    })
  }

  console.log('Lessons created')
  console.log('Seeding completed!')
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })
