"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Lock, Mail, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        setError("Đăng nhập thất bại. Vui lòng kiểm tra lại email và mật khẩu.");
      } else {
        router.push("/");
        router.refresh();
      }
    } catch (err) {
      setError("Không thể kết nối đến máy chủ.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-[420px] animate-in fade-in duration-500">
      <Card className="border-zinc-200 shadow-xl bg-white">
        <CardHeader className="space-y-3 pb-8 text-center">
          <div className="mx-auto w-12 h-12 bg-zinc-900 rounded-2xl flex items-center justify-center mb-2 shadow-lg">
            <Lock className="text-white h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">Hệ thống PaperSum</CardTitle>
          <CardDescription className="text-zinc-500">
            Đăng nhập để quản lý và theo dõi các bài báo khoa học
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleLogin}>
          <CardContent className="space-y-6">
            {error && (
              <Alert variant="destructive" className="py-3">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription className="text-xs font-medium">{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2.5">
              <Label htmlFor="email" className="text-xs font-bold uppercase tracking-widest text-zinc-400 ml-1">
                Địa chỉ Email
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3.5 h-4 w-4 text-zinc-400" />
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="admin@gmail.com" 
                  className="h-12 pl-10 bg-zinc-50/50 border-zinc-200 focus:bg-white transition-all" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required 
                />
              </div>
            </div>
            
            <div className="space-y-2.5 mb-4">
              <div className="flex justify-between items-center px-1">
                <Label htmlFor="password" className="text-xs font-bold uppercase tracking-widest text-zinc-400">
                  Mật khẩu
                </Label>
              </div>
              <Input 
                id="password" 
                type="password" 
                placeholder="••••••••" 
                className="h-12 bg-zinc-50/50 border-zinc-200 focus:bg-white transition-all" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required 
              />
            </div>
          </CardContent>

          <CardFooter className="flex flex-col gap-6 pt-8 pb-10">
            <Button className="w-full h-12 bg-zinc-900 hover:bg-zinc-800 text-white font-bold transition-all" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> 
                  Đang xác thực...
                </>
              ) : "Đăng nhập ngay"}
            </Button>
            
            <p className="text-center text-sm text-zinc-500">
              Chưa có tài khoản?{" "}
              <Link href="/register" className="text-zinc-900 hover:underline font-bold transition-all">
                Đăng ký thành viên
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}