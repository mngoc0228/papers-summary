import Navbar from "@/components/Navbar";
import AuthProvider from "@/components/AuthProvider";
import { Toaster } from "@/components/ui/sonner"

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
      <AuthProvider>
        <div className="relative min-h-screen flex flex-col bg-[#fafafa]">
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <div className="absolute -top-[10%] -left-[10%] size-[40%] rounded-full bg-zinc-100/50 blur-[120px]" />
            <div className="absolute -bottom-[10%] -right-[10%] size-[40%] rounded-full bg-zinc-100/50 blur-[120px]" />
          </div>
  
          <Navbar />
          
          <main className="relative flex-grow flex items-center justify-center py-16 px-4">
            {children}
          </main>
          <Toaster />
  
          <footer className="border-t bg-white/50 backdrop-blur-sm py-6" suppressHydrationWarning>
            <div className="container max-w-7xl mx-auto px-4 text-center text-xs text-zinc-400 font-medium" suppressHydrationWarning>
              © {new Date().getFullYear()} PaperSum - Công cụ tóm tắt nghiên cứu khoa học chuyên nghiệp.
            </div>
          </footer>
        </div>
      </AuthProvider>
    );
}
