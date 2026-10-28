import { http } from "./http";
import type { CreateOrderPayload, CreateOrderResponse, OrderDetail, OrderListQuery, OrderSummary } from "../types/order";
import type { PaginatedResponse } from "../types/api";

export const orderApi = {
  create: (payload: CreateOrderPayload) => http.post<CreateOrderResponse>("orders", payload),
  list: (params: OrderListQuery = {}) => {
    const query = new URLSearchParams({ page: String(params.page ?? 1), page_size: String(params.page_size ?? 10) });
    return http.get<PaginatedResponse<OrderSummary>>(`orders?${query.toString()}`);
  },
  detail: (id: number) => http.get<OrderDetail>(`orders/${id}`),
  cancel: (id: number) => http.post<{ id: number; status: "CANCELED"; message: string }>(`orders/${id}/cancel`, {}),
};
