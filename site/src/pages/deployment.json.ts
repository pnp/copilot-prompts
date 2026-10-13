import type { APIRoute } from "astro";

export const GET: APIRoute = () =>
  new Response(
    JSON.stringify({
      commit: import.meta.env.PUBLIC_COMMIT_SHA ?? "local",
      generatedAt: new Date().toISOString(),
    }),
    {
      headers: { "Content-Type": "application/json; charset=utf-8" },
    },
  );
