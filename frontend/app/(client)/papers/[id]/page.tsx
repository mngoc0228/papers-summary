import { apiRequest } from "@/lib/api";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Calendar, User, ExternalLink } from "lucide-react"; // Thêm ExternalLink
import { Button } from "@/components/ui/button"; // Thêm Button
import IPaper from "@/types";

export default async function PaperDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let paper:  IPaper;
  try {
    const response = await apiRequest(`/papers/${id}`);
    paper = response.data;
  } catch {
    return <div className="text-center py-20 text-red-500">Đã xảy ra lỗi khi tải bài báo.</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="space-y-4">
        {
          paper.topics.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {paper.topics.map((topic) => (
                <Badge key={topic.id} variant="secondary" className="bg-zinc-100 text-zinc-600 border-none font-bold text-[10px] uppercase px-2 py-0.5">
                  {topic.name}
                </Badge>
              ))}
            </div>
          )
        }
        <h1 className="text-4xl font-extrabold tracking-tight text-zinc-900">{paper.title}</h1>
        
        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-1.5">
            <User className="h-4 w-4" /> 
            {Array.isArray(paper.authors) && paper.authors.length > 2
              ? `${paper.authors.slice(0, 4).join(", ")} và ${paper.authors.length - 4} tác giả khác.`
              : Array.isArray(paper.authors)
                ? paper.authors.join(", ")
                : paper.authors}
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar className="h-4 w-4" /> 
            {new Date(paper.published_date).toLocaleDateString('vi-VN')}
          </div>
        </div>
      </div>

      {paper.url && (
        <div className="pt-2">
          <Button variant="outline" size="sm" asChild className="gap-2 border-zinc-200 text-zinc-600 hover:text-zinc-900 shadow-sm transition-all">
            <a href={paper.url} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-4 w-4" />
              Xem nguồn bài báo gốc
            </a>
          </Button>
        </div>
      )}

      <Separator className="bg-zinc-100" />

      <Tabs defaultValue="summary" className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-zinc-100/50 p-1">
          <TabsTrigger value="summary" className="data-[state=active]:bg-white data-[state=active]:shadow-sm font-bold">
            Bản tóm tắt (AI Summary)
          </TabsTrigger>
          <TabsTrigger value="details" className="data-[state=active]:bg-white data-[state=active]:shadow-sm font-bold">
            Nội dung chi tiết
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="summary" className="mt-6">
          <div className="prose prose-slate max-w-none bg-zinc-50/50 p-8 rounded-2xl border border-zinc-100">
            <h3 className="text-lg font-bold mb-4 text-zinc-900">Tóm tắt nội dung chính:</h3>
            <div className="text-zinc-700 leading-relaxed whitespace-pre-wrap italic">
              &quot;{paper.summary || 'Không có tóm tắt.'}&quot;
            </div>
          </div>
        </TabsContent>

        <TabsContent value="details" className="mt-6">
          <div className="prose prose-slate max-w-none px-2">
            <div className="text-zinc-800 leading-relaxed">
              {paper.abstract}
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}