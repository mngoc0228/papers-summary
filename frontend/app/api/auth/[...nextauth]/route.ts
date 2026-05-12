import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { apiRequest } from "@/lib/api";

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "FastAPI",
      credentials: {
        email: { type: "text" },
        password: { type: "password" }
      },
      async authorize(credentials) {
        const authData = await apiRequest("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(credentials),
        });

        if (authData.data.access_token) {
          const userData = await apiRequest("/users/me", {
            method: "GET",
            headers: { 
              "Authorization": `Bearer ${authData.data.access_token}` 
            },
          });

          return {
            ...userData.data,
            access_token: authData.data.access_token,
          };
        }
        return null;
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }: any) {
      if (user) {
        token.access_token = user.access_token;
        token.is_admin = user.is_admin;
        token.full_name = user.full_name;
      }
      return token;
    },
    async session({ session, token }: any) {
      if (token) {
        session.user.access_token = token.access_token;
        session.user.is_admin = token.is_admin;
        session.user.name = token.full_name;
      }
      return session;
    },
  },
  pages: { signIn: "/login" }
});

export { handler as GET, handler as POST };