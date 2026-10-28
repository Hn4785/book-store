import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, } from "../types/api";
import { request, tokenStorage } from "./http";

afterEach(() => {
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("HTTP client", () => {
  it("returns JSON for successful response and attaches bearer token", async () => {
    tokenStorage.set("abc-token");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ ok: true }), { status: 200, headers: { "Content-Type": "application/json" } }));
    await expect(request<{ ok: boolean }>("books")).resolves.toEqual({ ok: true });
    expect(fetchMock.mock.calls[0][1]?.headers).toBeInstanceOf(Headers);
    expect((fetchMock.mock.calls[0][1]?.headers as Headers).get("Authorization")).toBe("Bearer abc-token");
  });

  it("normalizes validation errors", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ error: "VALIDATION_ERROR", message: "Invalid input", fields: { quantity: ["Must be greater than 0"] } }), { status: 400 }));
    await expect(request("cart/items", { method: "POST", body: { quantity: 0 } })).rejects.toMatchObject({ status: 400, code: "VALIDATION_ERROR", message: "Invalid input" });
  });

  it("provides a consistent unauthorized error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ error: "UNAUTHENTICATED" }), { status: 401 }));
    try { await request("auth/me"); } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect(error).toMatchObject({ status: 401, message: "Phiên đăng nhập không hợp lệ hoặc đã hết hạn." });
    }
  });

  it("handles server errors", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ error: "INTERNAL_ERROR" }), { status: 500 }));
    await expect(request("books")).rejects.toMatchObject({ status: 500, message: "Máy chủ đang gặp sự cố. Vui lòng thử lại sau." });
  });

  it("handles a network failure", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("Failed to fetch"));
    await expect(request("books")).rejects.toMatchObject({ status: 0 });
  });
});
