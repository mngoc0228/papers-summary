import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, Users, Tags, TrendingUp } from "lucide-react";

export default function AdminDashboard() {
  const stats = [
    { name: "Tổng bài báo", value: "1,248", icon: BookOpen, change: "+12%" },
    { name: "Người dùng", value: "8,500", icon: Users, change: "+5%" },
    { name: "Chủ đề", value: "42", icon: Tags, change: "0%" },
    { name: "Lượt xem", value: "125.4K", icon: TrendingUp, change: "+18%" },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Tổng quan</h1>
        <p className="text-zinc-500 text-sm">Chào mừng bạn quay lại hệ thống quản trị.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <Card key={stat.name} className="border-zinc-200/60 shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xs font-bold uppercase tracking-wider text-zinc-500">
                {stat.name}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-zinc-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-[10px] text-zinc-400 font-bold mt-1">
                <span className="text-emerald-500 font-bold">{stat.change}</span> so với tháng trước
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Chỗ này sau này có thể thêm Biểu đồ hoặc Danh sách bài báo mới nhất */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 h-[300px] border-zinc-200/60 flex items-center justify-center text-zinc-300 italic text-sm">
          [Khu vực Biểu đồ Thống kê]
        </Card>
        <Card className="h-[300px] border-zinc-200/60 flex items-center justify-center text-zinc-300 italic text-sm">
          [Hoạt động gần đây]
        </Card>
      </div>
    </div>
  );
}