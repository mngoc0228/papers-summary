const getBaseUrl = () => {
  return typeof window === "undefined" || typeof window === undefined
    ? process.env.API_URL_SERVER ||
        process.env.NEXT_PUBLIC_API_URL ||
        "http://localhost:8000"
    : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
};

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const baseUrl = getBaseUrl();
  const res = await fetch(`${baseUrl}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Có lỗi xảy ra");
  }

  return res.json();
}
