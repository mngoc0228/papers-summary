import { apiRequest } from "@/lib/api";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, ChevronRight, Sparkles } from "lucide-react";

export default async function HomePage() {
  const papers = await apiRequest("/papers?page=1&size=6", {
    cache: "no-store",
  }).catch((e) => {
    console.error("Failed to fetch papers:", e);
    return { data: [] };
  });

  return (
    <div className="flex flex-col gap-20 pb-20">
      {/* Hero Section */}
      <section className="pt-20 pb-12 flex flex-col items-center text-center gap-6">
        <Badge
          variant="secondary"
          className="px-3 py-1 rounded-full flex gap-2 items-center"
        >
          <Sparkles className="h-3.5 w-3.5" />
          <span>Đã cập nhật hơn 500 bài báo mới</span>
        </Badge>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight max-w-4xl">
          Nghiên cứu khoa học <br /> tinh gọn hơn bao giờ hết.
        </h1>
        <p className="text-muted-foreground text-lg md:text-xl max-w-2xl">
          Sử dụng trí tuệ nhân tạo để tóm tắt những nghiên cứu phức tạp thành
          nội dung dễ hiểu.
        </p>
        <div className="flex gap-4 mt-4">
          <Button size="lg" className="h-12 px-8" asChild>
            <Link href="/papers">
              Khám phá thư viện <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Featured Section */}
      <section className="container max-w-7xl mx-auto space-y-10">
        <div className="flex justify-between items-end">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">
              Nghiên cứu mới nhất
            </h2>
            <p className="text-muted-foreground">
              Các công trình nghiên cứu vừa được tóm tắt.
            </p>
          </div>
          <Button variant="ghost" asChild>
            <Link href="/papers">
              Tất cả bài báo <ChevronRight className="ml-1 h-4 w-4" />
            </Link>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {papers.data?.map((paper: any) => (
            <Card
              key={paper.id}
              className="border-border/50 shadow-none hover:border-primary/30 transition-all bg-card/50"
            >
              <CardHeader className="space-y-4">
                {paper.topics && paper.topics.length > 0 && (
                  <Badge
                    variant="outline"
                    className="w-fit border-primary/20 text-primary/80"
                  >
                    {paper.topics
                      .map((topic: { name: string }) => topic.name)
                      .join(", ")}
                  </Badge>
                )}
                <CardTitle className="text-xl leading-snug line-clamp-2">
                  {paper.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed line-clamp-3">
                  {paper.summary}
                </CardDescription>
              </CardContent>
              <CardFooter className="pt-4 flex justify-between items-center border-t border-border/40">
                <span className="text-xs text-muted-foreground font-medium">
                  Tác giả: {paper.authors.join(", ")}
                </span>
                <Button
                  variant="link"
                  className="p-0 h-auto text-primary"
                  asChild
                >
                  <Link href={`/papers/${paper.id}`}>Đọc tiếp</Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </section>

      {/* Newsletter / CTA */}
      <section className="container max-w-7xl mx-auto py-12 px-8 rounded-3xl border bg-secondary/30 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-2">
          <h3 className="text-2xl font-bold tracking-tight">
            Đừng bỏ lỡ nghiên cứu mới
          </h3>
          <p className="text-muted-foreground">
            Nhận bản tin tóm tắt hàng tuần về các chủ đề bạn quan tâm.
          </p>
        </div>
        <div className="flex max-w-sm items-center space-x-2">
          <Button size="lg" className="w-full md:w-auto">
            Đăng ký nhận tin
          </Button>
        </div>
      </section>
    </div>
  );
}
