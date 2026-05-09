"use client";
import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export default function MyPage() {
  const { data: session }: any = useSession();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (session?.user?.access_token) {
      apiRequest("/users/me/dashboard", {
        headers: { Authorization: `Bearer ${session.user.access_token}` }
      }).then(setData);
    }
  }, [session]);

  return (
    <div className="space-y-10">
      {/* Profile Header */}
      <div className="flex items-center gap-4 bg-slate-50 p-8 rounded-2xl border">
        <Avatar className="h-20 w-20 border-2 border-primary">
          <AvatarFallback className="text-2xl">{session?.user?.name?.[0]}</AvatarFallback>
        </Avatar>
        <div>
          <h1 className="text-3xl font-bold">{session?.user?.name}</h1>
          <p className="text-muted-foreground">{session?.user?.email}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Followed Topics */}
        <Card shadow-sm>
          <CardHeader>
            <CardTitle>Chủ đề đang theo dõi</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {data?.followed_topics?.map((topic: any) => (
              <Badge key={topic.id} variant="secondary" className="px-3 py-1">
                {topic.name}
              </Badge>
            ))}
          </CardContent>
        </Card>

        {/* Favorite Papers */}
        <Card shadow-sm>
          <CardHeader>
            <CardTitle>Bài báo yêu thích</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {data?.favorite_papers?.map((paper: any) => (
              <div key={paper.id} className="flex justify-between items-center p-3 hover:bg-slate-50 rounded-md border transition-colors">
                <span className="font-medium line-clamp-1">{paper.title}</span>
                <Badge variant="outline">Đọc</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}