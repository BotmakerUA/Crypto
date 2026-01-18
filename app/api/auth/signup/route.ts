import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import bcrypt from 'bcryptjs'

export async function POST(req: Request) {
  try {
    const { email, phone, password } = await req.json()

    if (!email && !phone) {
      return NextResponse.json(
        { error: 'Email або телефон обов\'язкові' },
        { status: 400 }
      )
    }

    if (!password || password.length < 6) {
      return NextResponse.json(
        { error: 'Пароль повинен бути мінімум 6 символів' },
        { status: 400 }
      )
    }

    // Check if user exists
    const existingUser = await prisma.user.findFirst({
      where: {
        OR: [
          { email: email || undefined },
          { phone: phone || undefined },
        ],
      },
    })

    if (existingUser) {
      return NextResponse.json(
        { error: 'Користувач з таким email або телефоном вже існує' },
        { status: 400 }
      )
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10)

    // Create user
    const user = await prisma.user.create({
      data: {
        email: email || null,
        phone: phone || null,
        passwordHash,
      },
    })

    return NextResponse.json(
      { message: 'Користувач створений', userId: user.id },
      { status: 201 }
    )
  } catch (error) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { error: 'Внутрішня помилка сервера' },
      { status: 500 }
    )
  }
}
