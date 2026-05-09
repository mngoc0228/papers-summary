import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "FastAPI",
      credentials: {
        email: { type: "text" },
        password: { type: "password" }
      },
      async authorize(credentials) {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(credentials),
        });

        const authData = await res.json();        

        if (res.ok && authData.data.access_token) {
          const userRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/me`, {
            method: "GET",
            headers: { 
              "Authorization": `Bearer ${authData.data.access_token}` 
            },
          });

          const userData = await userRes.json();

          if (userRes.ok) {
            return {
              ...userData.data,
              access_token: authData.data.access_token,
            };
          }
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