import { type ClassValue, clsx } from 'clsx'

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}

export function getLocalizedContent(content: any, locale: string) {
  if (typeof content === 'string') return content
  return content?.[locale] || content?.['uk'] || content?.['en'] || ''
}

export function formatPrice(price: number, currency: string = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(price / 100)
}

export function calculateEndDate(startDate: Date, days: number): Date {
  const endDate = new Date(startDate)
  endDate.setDate(endDate.getDate() + days)
  return endDate
}

export function isSubscriptionActive(subscription: { endDate: Date; status: string }): boolean {
  return subscription.status === 'ACTIVE' && new Date() < new Date(subscription.endDate)
}
