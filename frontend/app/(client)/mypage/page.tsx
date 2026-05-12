"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { apiRequest } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { User, Calendar, BookOpen, Tags, ArrowRight, Star, Library, LayoutGrid } from "lucide-react";
import { IPaper, ITopic } from "@/types";
import { Button } from "@/components/ui/button";

export default function MyPage() {
  const { data: session }: any = useSession();
  const [followedTopics, setFollowedTopics] = useState<ITopic[]>([]);
  const [favoritePapers, setFavoritePapers] = useState<IPaper[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (session?.user?.access_token) {
      const headers = { Authorization: `Bearer ${session.user.access_token}` };

      const fetchDashboardData = async () => {
        setLoading(true);
        try {
          // Giữ nguyên API của bạn nhưng sửa lại thứ tự gán biến để đúng logic dữ liệu
          const [favRes, topicRes] = await Promise.all([
            apiRequest("/papers/favorites", { headers }),
            apiRequest("/topics/followed", { headers })
          ]);
          
          setFavoritePapers(favRes.data || []);
          setFollowedTopics(topicRes.data || []);
        } catch (error) {
          console.error("Lỗi khi tải dữ liệu:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchDashboardData();
    }
  }, [session]);

  if (loading) {
    return <div className="max-w-4xl mx-auto py-20 text-center text-zinc-400 animate-pulse">Đang tải dữ liệu...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-10 py-6 animate-in fade-in duration-700">
      
      {/* 1. Profile Header - Được tinh chỉnh để trông cao cấp hơn */}
      <div className="flex flex-col md:flex-row items-center gap-6 p-10 rounded-[2rem] border border-zinc-100 bg-white shadow-sm shadow-zinc-200/50">
        <div className="h-20 w-20 rounded-2xl bg-zinc-900 flex items-center justify-center text-white text-3xl font-bold shadow-xl shadow-zinc-200">
          {session?.user?.name?.[0] || <User className="h-10 w-10" />}
        </div>
        <div className="text-center md:text-left space-y-1">
          <h1 className="text-3xl font-black tracking-tight text-zinc-900">{session?.user?.name || "Người dùng"}</h1>
          <p className="text-zinc-500 font-medium">{session?.user?.email}</p>
          <div className="pt-2">
             <Badge variant="outline" className="bg-zinc-50 text-[10px] font-bold uppercase tracking-widest text-zinc-400 border-zinc-200">
                Tài khoản học thuật
             </Badge>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* 2. Followed Topics Section - Cột bên trái */}
        <div className="lg:col-span-1 space-y-6">
          <div className="flex items-center gap-2 px-1">
            <Tags className="h-5 w-5 text-zinc-900" />
            <h2 className="font-bold text-lg text-zinc-900 tracking-tight">Chủ đề quan tâm</h2>
          </div>
          
          <div className="bg-zinc-50/50 border border-zinc-100 p-5 rounded-2xl space-y-4">
            <div className="flex flex-wrap gap-2">
              {followedTopics.length > 0 ? (
                followedTopics.map((topic) => (
                  <Link key={topic.id} href={`/papers?topic=${topic.id}`}>
                    <Badge 
                      variant="secondary" 
                      className="bg-white text-zinc-600 hover:bg-zinc-900 hover:text-white transition-all border border-zinc-200 shadow-sm font-bold text-[10px] uppercase px-3 py-1 cursor-pointer w-fit"
                    >
                      {topic.name}
                    </Badge>
                  </Link>
                ))
              ) : (
                <p className="text-xs text-zinc-400 italic py-2">Bạn chưa theo dõi chủ đề nào.</p>
              )}
            </div>
            
            <Separator className="bg-zinc-200/50" />
            
            <Button variant="ghost" size="sm" className="w-full text-zinc-400 hover:text-zinc-900 text-[11px] font-bold uppercase tracking-tighter" asChild>
              <Link href="/papers" className="flex items-center justify-center gap-2">
                <LayoutGrid className="h-3 w-3" />
                Khám phá thêm chủ đề
              </Link>
            </Button>
          </div>
        </div>

        {/* 3. Favorite Papers Section - Cột chính bên phải */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <Star className="h-5 w-5 text-zinc-900 fill-zinc-900" />
              <h2 className="font-bold text-lg text-zinc-900 tracking-tight">Thư viện yêu thích</h2>
            </div>
            <Badge className="bg-zinc-100 text-zinc-900 border-none font-bold">{favoritePapers.length} bài báo</Badge>
          </div>

          <div className="grid gap-4">
            {favoritePapers.length > 0 ? (
              favoritePapers.map((paper) => (
                <Card key={paper.id} className="group border-zinc-100 hover:border-zinc-300 transition-all shadow-sm hover:shadow-md rounded-2xl overflow-hidden bg-white">
                  <CardHeader className="p-6 space-y-3">
                    <div className="flex justify-between items-start">
                      <div className="flex flex-wrap gap-2">
                        {paper.topics?.slice(0, 2).map((topic) => (
                          <Badge key={topic.id} variant="secondary" className="bg-zinc-50 text-zinc-400 border-none font-bold text-[9px] uppercase px-2 py-0.5">
                            {topic.name}
                          </Badge>
                        ))}
                      </div>
                      <span className="flex items-center gap-1.5 text-[10px] font-bold text-zinc-300 uppercase tracking-widest">
                        <Calendar className="h-3 w-3" />
                        {new Date(paper.published_date).getFullYear()}
                      </span>
                    </div>

                    <Link href={`/papers/${paper.id}`}>
                      <CardTitle className="text-xl font-bold leading-tight group-hover:text-zinc-600 transition-colors decoration-zinc-200 underline-offset-4 group-hover:underline">
                        {paper.title}
                      </CardTitle>
                    </Link>

                    <CardDescription className="text-zinc-500 text-sm line-clamp-2 italic leading-relaxed">
                      &quot;{paper.summary || paper.abstract || "Không có tóm tắt"}&quot;
                    </CardDescription>

                    <div className="pt-3 flex justify-between items-center border-t border-zinc-50 mt-2">
                       <div className="flex items-center gap-2 text-xs text-zinc-400 font-medium">
                          <User className="h-3.5 w-3.5" />
                          <span className="line-clamp-1">
                            {Array.isArray(paper.authors) && paper.authors.join(", ")}
                          </span>
                       </div>
                       <Button variant="link" size="sm" className="h-auto p-0 text-zinc-900 font-bold group-hover:gap-2 transition-all" asChild>
                         <Link href={`/papers/${paper.id}`}>
                            Đọc tiếp <ArrowRight className="h-3 w-3" />
                         </Link>
                       </Button>
                    </div>
                  </CardHeader>
                </Card>
              ))
            ) : (
              <div className="text-center py-20 border-2 border-dashed border-zinc-100 rounded-[2rem] bg-zinc-50/30">
                <BookOpen className="h-12 w-12 text-zinc-200 mx-auto mb-4" />
                <p className="text-zinc-500 font-bold">Chưa có bài báo nào trong thư viện</p>
                <p className="text-xs text-zinc-400 mt-1 mb-6">Hãy đánh dấu yêu thích các bài báo để lưu trữ tại đây.</p>
                <Button size="sm" asChild>
                  <Link href="/papers">Khám phá thư viện</Link>
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}