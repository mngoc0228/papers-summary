import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  logging: {
    fetches: {
      fullUrl: true,
    },
    browserToTerminal: true,
  },
};

export default nextConfig;
