"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { 
  LayoutDashboard, 
  Users, 
  BookOpen, 
  Tags, 
  Settings, 
  LogOut, 
  ExternalLink 
} from "lucide-react";

const menuItems = [
  { name: "Tổng quan", href: "/admin", icon: LayoutDashboard },
  { name: "Quản lý Bài báo", href: "/admin/papers", icon: BookOpen },
  { name: "Quản lý Chủ đề", href: "/admin/topics", icon: Tags },
  { name: "Người dùng", href: "/admin/users", icon: Users },
];

export default function AdminSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-zinc-50/50 flex flex-col h-screen sticky top-0">
      {/* Logo Admin */}
      <div className="p-6">
        <Link href="/admin" className="flex items-center gap-2 font-bold text-xl tracking-tighter">
          <div className="w-8 h-8 bg-zinc-900 rounded-lg flex items-center justify-center text-white text-sm">
            PS
          </div>
          <span>PaperAdmin</span>
        </Link>
      </div>

      {/* Menu chính */}
      <nav className="flex-1 px-4 space-y-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}>
              <span className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-all group",
                isActive 
                  ? "bg-zinc-900 text-white shadow-md shadow-zinc-200" 
                  : "text-zinc-500 hover:bg-zinc-200/50 hover:text-zinc-900"
              )}>
                <item.icon className={cn("h-4 w-4", isActive ? "text-white" : "text-zinc-400 group-hover:text-zinc-900")} />
                {item.name}
              </span>
            </Link>
          );
        })}
      </nav>

      {/* Footer Sidebar */}
      <div className="p-4 mt-auto space-y-2">
        <Button variant="outline" className="w-full justify-start gap-2 border-zinc-200 text-zinc-500" asChild>
          <Link href="/"><ExternalLink className="h-4 w-4" /> Về trang Client</Link>
        </Button>
        <Button variant="ghost" className="w-full justify-start gap-2 text-zinc-500 hover:text-destructive">
          <LogOut className="h-4 w-4" /> Đăng xuất
        </Button>
      </div>
    </aside>
  );
}