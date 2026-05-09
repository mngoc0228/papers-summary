import AdminSidebar from "@/components/AdminSidebar";
import AuthProvider from "@/components/AuthProvider";
import { Separator } from "@/components/ui/separator";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <div className="flex min-h-screen bg-white">
        {/* Sidebar cố định bên trái */}
        <AdminSidebar />

        {/* Nội dung chính bên phải */}
        <div className="flex-1 flex flex-col">
          {/* Header nhẹ phía trên nội dung */}
          <header className="h-16 border-b flex items-center justify-between px-8 bg-white/80 backdrop-blur-md sticky top-0 z-40">
            <div className="text-sm font-medium text-zinc-500">
              Trang quản trị / <span className="text-zinc-900">Hệ thống</span>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-bold text-zinc-900">Khai Nguyen</p>
                <p className="text-[10px] text-zinc-400 uppercase tracking-widest font-bold">Quản trị viên</p>
              </div>
              <div className="w-8 h-8 rounded-full bg-zinc-100 border border-zinc-200 flex items-center justify-center font-bold text-xs">
                KN
              </div>
            </div>
          </header>

          {/* Khu vực chứa nội dung các trang con */}
          <main className="p-8 bg-zinc-50/30 flex-1">
            <div className="max-w-6xl mx-auto">
              {children}
            </div>
          </main>
        </div>
      </div>
    </AuthProvider>
  );
}