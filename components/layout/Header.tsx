'use client'

import { useTranslations } from 'next-intl'
import Link from 'next/link'
import { useSession, signOut } from 'next-auth/react'
import ThemeToggle from '@/components/ui/ThemeToggle'
import LanguageSwitcher from '@/components/ui/LanguageSwitcher'

export default function Header() {
  const t = useTranslations()
  const { data: session } = useSession()

  return (
    <header className="bg-white dark:bg-background-dark shadow-sm sticky top-0 z-50">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-primary">
            {t('common.appName')}
          </Link>

          <div className="hidden md:flex items-center space-x-6">
            <Link href="/" className="hover:text-primary transition-colors">
              {t('nav.home')}
            </Link>
            {session && (
              <>
                <Link href="/lessons" className="hover:text-primary transition-colors">
                  {t('nav.lessons')}
                </Link>
                <Link href="/dashboard" className="hover:text-primary transition-colors">
                  {t('nav.dashboard')}
                </Link>
                {session.user.role === 'ADMIN' && (
                  <Link href="/admin" className="hover:text-primary transition-colors">
                    {t('nav.admin')}
                  </Link>
                )}
              </>
            )}
          </div>

          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            <ThemeToggle />
            {session ? (
              <button
                onClick={() => signOut()}
                className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
              >
                {t('common.signOut')}
              </button>
            ) : (
              <Link
                href="/auth/signin"
                className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
              >
                {t('common.signIn')}
              </Link>
            )}
          </div>
        </div>
      </nav>
    </header>
  )
}
