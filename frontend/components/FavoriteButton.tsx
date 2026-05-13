"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Star, Loader2 } from "lucide-react";
import { apiRequest } from "@/lib/api";
import { useSession } from "next-auth/react";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export default function FavoriteButton({
  paperId,
  initialIsFavorite,
}: {
  paperId: string;
  initialIsFavorite: boolean;
}) {
  const { data: session }: any = useSession();
  const [isFavorite, setIsFavorite] = useState(initialIsFavorite);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const toggleFavorite = async () => {
    if (!session) {
      return toast.error("Yêu cầu đăng nhập", {
        description: "Vui lòng đăng nhập để lưu bài báo vào thư viện.",
        action: {
          label: "Đăng nhập",
          onClick: () => router.push("/login"),
        },
      });
    }

    setLoading(true);
    try {
      const promise = async () => {
        const method = isFavorite ? "DELETE" : "POST";
        await apiRequest(`/papers/${paperId}/favorites`, {
          method,
          headers: { Authorization: `Bearer ${session.user.access_token}` },
        });
        setIsFavorite(!isFavorite);
        return !isFavorite;
      };

      toast.promise(promise(), {
        loading: "Đang xử lý...",
        success: (data) => {
          return data ? "Đã lưu vào thư viện" : "Đã xóa khỏi thư viện";
        },
        error: "Có lỗi xảy ra, vui lòng thử lại.",
      });
    } catch (error) {
      console.error("Lỗi favorite:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={toggleFavorite}
      disabled={loading}
      className={cn(
        "gap-2 border-zinc-200 transition-all",
        isFavorite &&
          "bg-zinc-900 text-white border-zinc-900 hover:bg-zinc-800",
      )}
    >
      {loading ? (
        <Loader2 className="h-4 w-4 animate-spin" />
      ) : (
        <Star className={cn("h-4 w-4", isFavorite && "fill-current")} />
      )}
      {isFavorite ? "Đã lưu" : "Lưu bài báo"}
    </Button>
  );
}
