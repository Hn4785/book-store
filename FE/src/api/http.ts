import { ApiError, type ApiErrorBody } from "../types/api";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1").replace(/\/+$/, "");
const TOKEN_KEY = "bookshop_access_token";

export const tokenStorage = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
  auth?: boolean;
};

function buildUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
}

function extractMessage(body: ApiErrorBody | undefined, status: number): string {
  if (body?.message && typeof body.message === "string") return body.message;
  if (body?.detail && typeof body.detail === "string") return body.detail;
  if (body?.fields) {
    const first = Object.values(body.fields)[0];
    if (Array.isArray(first)) return first[0] || "Dữ liệu không hợp lệ.";
    if (typeof first === "string") return first;
  }
  if (status === 401) return "Phiên đăng nhập không hợp lệ hoặc đã hết hạn.";
  if (status === 403) return "Bạn không có quyền thực hiện thao tác này.";
  if (status === 404) return "Không tìm thấy dữ liệu yêu cầu.";
  if (status >= 500) return "Máy chủ đang gặp sự cố. Vui lòng thử lại sau.";
  return "Không thể thực hiện yêu cầu.";
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, auth = true, headers: customHeaders, ...rest } = options;
  const headers = new Headers(customHeaders);
  headers.set("Accept", "application/json");
  if (body !== undefined) headers.set("Content-Type", "application/json");
  if (auth) {
    const token = tokenStorage.get();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;
  try {
    response = await fetch(buildUrl(path), {
      ...rest,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError("Không thể kết nối backend. Hãy kiểm tra server và VITE_API_BASE_URL.", 0);
  }

  if (response.status === 204) return undefined as T;

  const raw = await response.text();
  let parsed: unknown;
  try { parsed = raw ? JSON.parse(raw) : undefined; } catch { parsed = undefined; }

  if (!response.ok) {
    const errorBody = parsed && typeof parsed === "object" ? parsed as ApiErrorBody : undefined;
    throw new ApiError(extractMessage(errorBody, response.status), response.status, errorBody);
  }
  return parsed as T;
}

export const http = {
  get: <T>(path: string, options?: RequestOptions) => request<T>(path, { ...options, method: "GET" }),
  post: <T>(path: string, body?: unknown, options?: RequestOptions) => request<T>(path, { ...options, method: "POST", body }),
  patch: <T>(path: string, body?: unknown, options?: RequestOptions) => request<T>(path, { ...options, method: "PATCH", body }),
  delete: <T>(path: string, options?: RequestOptions) => request<T>(path, { ...options, method: "DELETE" }),
};

export function apiBaseUrl(): string {
  return API_BASE_URL;
}
