"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { apiRequest } from "@/lib/api";
import { Loader2, UserPlus } from "lucide-react";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    full_name: "",
    avatar: ""
  });
  const [loading, setLoading] = useState(false);
  const { push } = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await apiRequest("/users", {
        method: "POST",
        body: JSON.stringify(formData),
      });
      push("/login?status=success");
    } catch (err) {
      alert("Đăng ký lỗi: Email có thể đã tồn tại.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-[420px] animate-in fade-in duration-500">
      <Card className="border-zinc-200 shadow-xl bg-white">
        <CardHeader className="space-y-3 pb-8 text-center">
          <div className="mx-auto size-12 bg-zinc-900 rounded-2xl flex items-center justify-center mb-2 shadow-lg">
            <UserPlus className="text-white size-6" />
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">Tạo tài khoản mới</CardTitle>
          <CardDescription className="text-zinc-500">Tham gia hệ thống tóm tắt báo khoa học</CardDescription>
        </CardHeader>

        <form onSubmit={handleRegister}>
          <CardContent className="space-y-5">
            <div className="space-y-2">
              <Label className="text-xs font-bold uppercase text-zinc-400">Họ và tên</Label>
              <Input 
                placeholder="Nguyễn Văn A" 
                className="h-12 bg-zinc-50/50" 
                onChange={e => setFormData(prev => ({...prev, full_name: e.target.value}))}
              />
            </div>
            <div className="space-y-2">
              <Label className="text-xs font-bold uppercase text-zinc-400">Email</Label>
              <Input 
                type="email" 
                placeholder="name@example.com" 
                className="h-12 bg-zinc-50/50" 
                onChange={e => setFormData(prev => ({...prev, email: e.target.value}))}
                required 
              />
            </div>
            <div className="space-y-2 mb-4">
              <Label className="text-xs font-bold uppercase text-zinc-400">Mật khẩu</Label>
              <Input 
                type="password" 
                className="h-12 bg-zinc-50/50" 
                onChange={e => setFormData(prev => ({...prev, password: e.target.value}))}
                required 
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-6 pt-8 pb-10">
            <Button className="w-full h-12 bg-zinc-900 hover:bg-zinc-800 text-white font-bold" disabled={loading}>
              {loading ? <Loader2 className="size-4 animate-spin" /> : "Đăng ký thành viên"}
            </Button>
            <p className="text-center text-sm text-zinc-500">
              Đã có tài khoản? <Link href="/login" className="text-zinc-900 font-bold hover:underline">Đăng nhập</Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}