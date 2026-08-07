import { QueryClient } from "@tanstack/react-query";
import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";

// Sub-path fix (see vault: 07 System/Mission Control/): this app is hosted under
// base "/mission-control/", but its /__* API calls are written root-absolute
// (e.g. fetch("/__live-data")). In the browser those must target the base, or the
// reverse proxy routes them to the "/" backend (Hermes) and all live data fails.
// One shim covers every /__* call site (current and future). Pairs with the
// rewrite middleware in vite.config.ts. Do NOT remove one without the other.
if (typeof window !== "undefined") {
  const _fetch = window.fetch.bind(window);
  const BASE = import.meta.env.BASE_URL.replace(/\/$/, ""); // "/mission-control"
  window.fetch = ((input: any, init?: any) => {
    if (typeof input === "string" && input.startsWith("/__")) input = BASE + input;
    return _fetch(input, init);
  }) as typeof window.fetch;
}

export const getRouter = () => {
  const queryClient = new QueryClient();

  const router = createRouter({
    routeTree,
    basepath: "/mission-control",
    context: { queryClient },
    scrollRestoration: true,
    defaultPreloadStaleTime: 0,
  });

  return router;
};
