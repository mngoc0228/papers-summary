"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { apiRequest } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Users, Sparkles, Calendar } from "lucide-react";
import IPaper from "@/types";

type PapersResponse = {
  data?: IPaper[];
  page?: number;
  size?: number;
  total?: number;
  pages?: number;
};

function getTotalPages(response: PapersResponse) {
  return response.pages ?? 1;
}

function getVisiblePages(currentPage: number, totalPages: number) {
  if (totalPages <= 3) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }
  if (currentPage <= 2) return [1, 2, 3];
  if (currentPage >= totalPages - 1)
    return [totalPages - 2, totalPages - 1, totalPages].filter((p) => p > 0);
  return [currentPage - 1, currentPage, currentPage + 1];
}

function PapersListContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pageSize = 12;

  const currentPage = Math.max(1, Number(searchParams.get("page") || 1));
  const selectedTopicId = searchParams.get("topic") || "";

  const [papers, setPapers] = useState<IPaper[]>([]);
  const [loading, setLoading] = useState(true);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const [topics, setTopics] = useState<{ id: string | number; name: string }[]>(
    [],
  );

  useEffect(() => {
    let active = true;
    async function loadPapers() {
      setLoading(true);
      try {
        let url = `/papers?page=${currentPage}&size=${pageSize}`;
        if (selectedTopicId) {
          url += `&topic_id=${selectedTopicId}`;
        }
        const response = (await apiRequest(url, {
          cache: "no-store",
        })) as PapersResponse;
        if (!active) return;
        const nextPapers = response.data || [];
        setPapers(nextPapers);
        const nextTotalPages = getTotalPages(response);
        setTotalPages(nextTotalPages);
        setHasNextPage(currentPage < nextTotalPages);
      } catch {
        if (active) {
          setPapers([]);
          setHasNextPage(false);
          setTotalPages(1);
        }
      } finally {
        if (active) setLoading(false);
      }
    }
    loadPapers();
    return () => {
      active = false;
    };
  }, [currentPage, selectedTopicId]);

  useEffect(() => {
    apiRequest(`/topics`, { cache: "no-store" })
      .then((res: any) => {
        setTopics(res.data ?? []);
      })
      .catch(() => setTopics([]));
  }, []);

  const updateFilters = (nextPage: number, nextTopicId?: string | null) => {
    const params = new URLSearchParams(searchParams.toString());
    if (nextPage <= 1) params.delete("page");
    else params.set("page", String(nextPage));
    if (nextTopicId === null) params.delete("topic");
    else if (nextTopicId !== undefined) params.set("topic", nextTopicId);
    router.push(`?${params.toString()}`);
  };

  const visiblePages = getVisiblePages(currentPage, totalPages);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-12 animate-in fade-in duration-700">
      <div className="flex flex-col gap-6 border-b pb-10">
        <div className="space-y-3">
          <Badge
            variant="outline"
            className="w-fit bg-zinc-50 text-zinc-500 border-zinc-200"
          >
            <Sparkles className="h-3 w-3 mr-2" /> Thư viện tri thức
          </Badge>
          <h1 className="text-4xl font-black tracking-tighter text-zinc-950">
            Thư viện bài báo
          </h1>
          <p className="text-zinc-500 text-base max-w-2xl leading-relaxed">
            Tiếp cận những nghiên cứu khoa học mới nhất, được tóm tắt súc tích
            giúp bạn tối ưu hóa thời gian nghiên cứu.
          </p>
        </div>
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400" />
          <Input
            placeholder="Tìm tên bài báo"
            className="pl-10 h-10 bg-white border-zinc-200 focus-visible:ring-zinc-900"
          />
        </div>
      </div>

      <div className="group relative">
        <div className="flex items-center gap-2 overflow-x-auto pb-3 flex-nowrap scrollbar-none [&::-webkit-scrollbar]:h-1.5 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-transparent group-hover:[&::-webkit-scrollbar-track]:bg-zinc-100 group-hover:[&::-webkit-scrollbar-thumb]:bg-zinc-300 group-hover:[&::-webkit-scrollbar-thumb]:rounded-full transition-all duration-300">
          <Button
            variant={selectedTopicId === "" ? "default" : "ghost"}
            size="sm"
            className="rounded-full px-5 h-8 text-xs shadow-none shrink-0"
            onClick={() => updateFilters(1, null)}
          >
            Tất cả
          </Button>
          {topics.map((topic) => (
            <Button
              key={topic.id}
              variant={
                selectedTopicId === String(topic.id) ? "default" : "ghost"
              }
              size="sm"
              className="rounded-full px-5 h-8 text-xs shadow-none shrink-0"
              onClick={() => updateFilters(1, String(topic.id))}
            >
              {topic.name}
            </Button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 min-h-[400px]">
        {loading ? (
          <div className="col-span-full text-center py-20 text-zinc-400">
            Đang tải bài báo...
          </div>
        ) : papers.length > 0 ? (
          papers.map((paper) => (
            <Card
              key={paper.id}
              className="group border-zinc-200/60 shadow-none hover:border-zinc-400 transition-all duration-300 bg-white flex flex-col rounded-xl overflow-hidden"
            >
              <CardHeader className="p-5 space-y-4">
                <div className="flex items-center justify-between w-full">
                  <div className="flex flex-wrap gap-2 justify-start">
                    {paper.topics?.map((topic) => (
                      <Badge
                        key={topic.name}
                        variant="secondary"
                        className="w-fit bg-zinc-100 text-zinc-600 border-none font-bold text-[10px] uppercase px-2 py-0.5"
                      >
                        {topic.name}
                      </Badge>
                    ))}
                  </div>
                  {paper.published_date && (
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                      <Calendar className="h-3 w-3" />
                      {new Date(paper.published_date).toLocaleDateString()}
                    </div>
                  )}
                </div>
                <CardTitle className="text-lg font-bold leading-snug group-hover:text-zinc-600 transition-colors line-clamp-2 min-h-[50px]">
                  <Link
                    href={`/papers/${paper.id}`}
                    className="hover:underline"
                  >
                    {paper.title}
                  </Link>
                </CardTitle>
              </CardHeader>
              <CardContent className="px-5 pb-5 flex-grow space-y-4">
                <div className="flex items-start gap-2 text-xs text-zinc-400 font-medium">
                  <Users className="h-3.5 w-3.5 shrink-0" />
                  <span className="line-clamp-1">
                    {Array.isArray(paper.authors) && paper.authors.length > 2
                      ? `${paper.authors.slice(0, 2).join(", ")} và nnk.`
                      : Array.isArray(paper.authors)
                        ? paper.authors.join(", ")
                        : paper.authors}
                  </span>
                </div>
                <p className="text-zinc-500 text-sm leading-relaxed line-clamp-3 italic">
                  &quot;{paper.summary || paper.abstract || "Không có tóm tắt"}
                  &quot;
                </p>
              </CardContent>
            </Card>
          ))
        ) : (
          <div className="col-span-full text-center py-20 text-zinc-400">
            Không tìm thấy bài báo nào cho chủ đề này.
          </div>
        )}
      </div>

      <div className="flex items-center justify-center gap-4 pt-10 border-t border-zinc-100">
        <Button
          variant="ghost"
          size="sm"
          className={
            currentPage > 1
              ? "text-zinc-900 text-xs font-bold"
              : "text-zinc-300 text-xs cursor-not-allowed"
          }
          disabled={currentPage <= 1 || loading}
          onClick={() => updateFilters(currentPage - 1)}
        >
          Trang trước
        </Button>
        <div className="flex items-center gap-1">
          {visiblePages.map((page) => (
            <Button
              key={page}
              variant={page === currentPage ? "outline" : "ghost"}
              size="sm"
              className={`h-8 w-8 text-xs ${page === currentPage ? "border-zinc-900 font-bold text-zinc-950" : "text-zinc-400"}`}
              onClick={() => updateFilters(page)}
            >
              {page}
            </Button>
          ))}
        </div>
        <Button
          variant="ghost"
          size="sm"
          className={
            hasNextPage
              ? "text-zinc-900 text-xs font-bold"
              : "text-zinc-300 text-xs cursor-not-allowed"
          }
          disabled={!hasNextPage || loading}
          onClick={() => updateFilters(currentPage + 1)}
        >
          Trang tiếp
        </Button>
      </div>
    </div>
  );
}

export default function PapersPage() {
  return (
    <Suspense
      fallback={
        <div className="max-w-6xl mx-auto px-4 py-10 text-center text-zinc-400">
          Đang tải trang...
        </div>
      }
    >
      <PapersListContent />
    </Suspense>
  );
}
