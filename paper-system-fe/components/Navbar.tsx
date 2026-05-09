"use client";
import Link from "next/link";
import { useSession, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { BookOpenText } from "lucide-react";

export default function Navbar() {
  const { data: session }: any = useSession();  

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between max-w-7xl mx-auto px-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tighter">
          <BookOpenText className="h-6 w-6" />
          <span>PaperSum</span>
        </Link>

        <div className="flex items-center gap-6">
          <nav className="hidden md:flex gap-6 items-center">
            <Link href="/papers" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Khám phá
            </Link>
            {session?.user?.is_admin && (
              <Link href="/admin" className="text-sm font-semibold text-primary">
                Quản trị
              </Link>
            )}
          </nav>

          <div className="flex items-center gap-2 border-l pl-6">
            {session ? (
              <>
                <Button variant="ghost" asChild size="sm">
                  <Link href="/mypage">Tài khoản</Link>
                </Button>
                <Button variant="outline" size="sm" onClick={() => signOut()}>
                  Đăng xuất
                </Button>
              </>
            ) : (
              <>
                <Button variant="ghost" asChild size="sm">
                  <Link href="/login">Đăng nhập</Link>
                </Button>
                <Button size="sm" asChild>
                  <Link href="/register">Bắt đầu ngay</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}