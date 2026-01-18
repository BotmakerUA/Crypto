import { NextResponse } from 'next/server'
import { headers } from 'next/headers'
import { stripe } from '@/lib/stripe/client'
import { prisma } from '@/lib/db'
import { calculateEndDate } from '@/lib/utils'

export async function POST(req: Request) {
  const body = await req.text()
  const signature = headers().get('stripe-signature')

  if (!signature) {
    return NextResponse.json({ error: 'No signature' }, { status: 400 })
  }

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )

    if (event.type === 'checkout.session.completed') {
      const session = event.data.object as any

      const userId = session.metadata.userId
      const plan = session.metadata.plan
      const isLifetime = plan === 'lifetime'

      // Create payment record
      await prisma.payment.create({
        data: {
          userId,
          amount: session.amount_total,
          currency: session.currency,
          status: 'SUCCEEDED',
          stripePaymentId: session.payment_intent,
          type: 'COURSE_PURCHASE',
        },
      })

      // Get the course
      const course = await prisma.course.findFirst({
        where: { isPublished: true },
      })

      if (course) {
        // Create or update subscription
        const endDate = isLifetime
          ? new Date(Date.now() + 100 * 365 * 24 * 60 * 60 * 1000) // 100 years
          : calculateEndDate(new Date(), course.durationDays)

        await prisma.subscription.create({
          data: {
            userId,
            courseId: course.id,
            status: 'ACTIVE',
            startDate: new Date(),
            endDate,
            isLifetime,
          },
        })
      }
    }

    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('Webhook error:', error)
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 400 }
    )
  }
}
