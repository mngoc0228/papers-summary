import "./globals.css";
import { Inter } from "next/font/google";
import { cn } from "@/lib/utils"; // Hàm cn dùng để gộp class của Shadcn
import AuthProvider from "@/components/AuthProvider";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <body className={cn(
        "min-h-screen bg-background font-sans antialiased",
        inter.className
      )}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}