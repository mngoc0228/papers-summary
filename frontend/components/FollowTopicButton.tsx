"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { apiRequest } from "@/lib/api";
import { useSession } from "next-auth/react";
import { Plus, Check, Loader2 } from "lucide-react";

export default function FollowTopicButton({ topicId, topicName, initialIsFollowed }: { topicId: string, topicName: string, initialIsFollowed: boolean }) {
  const { data: session }: any = useSession();
  const [isFollowed, setIsFollowed] = useState(initialIsFollowed);
  const [loading, setLoading] = useState(false);

  const handleFollow = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!session) return alert("Vui lòng đăng nhập");
    
    setLoading(true);
    try {
      const endpoint = isFollowed ? "unfollow" : "follow";
      await apiRequest(`/topics/${topicId}/${endpoint}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${session.user.access_token}` }
      });
      setIsFollowed(!isFollowed);
    } catch (error) {
      console.error("Lỗi follow topic:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Badge 
      variant={isFollowed ? "default" : "secondary"}
      onClick={handleFollow}
      className="cursor-pointer gap-1 px-2 py-0.5 font-bold text-[10px] uppercase transition-all"
    >
      {topicName}
      {loading ? <Loader2 className="h-2 w-2 animate-spin" /> : (isFollowed ? <Check className="h-2 w-2" /> : <Plus className="h-2 w-2" />)}
    </Badge>
  );
}