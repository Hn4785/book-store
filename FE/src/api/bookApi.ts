import { http } from "./http";
import type { Book, BookQuery } from "../types/book";
import type { PaginatedResponse } from "../types/api";

function queryString(params: Record<string, string | number | undefined>): string {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") query.set(key, String(value));
  });
  const encoded = query.toString();
  return encoded ? `?${encoded}` : "";
}

export const bookApi = {
  list: (params: BookQuery = {}) =>
    http.get<PaginatedResponse<Book>>(`books${queryString({ search: params.search, page: params.page ?? 1, page_size: params.page_size ?? 10 })}`, { auth: false }),
  detail: (id: number) => http.get<Book>(`books/${id}`, { auth: false }),
};
