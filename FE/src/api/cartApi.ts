import { http } from "./http";
import type { AddCartItemPayload, Cart, CartItemMutationResponse, UpdateCartItemPayload } from "../types/cart";

export const cartApi = {
  get: () => http.get<Cart>("cart"),
  add: (payload: AddCartItemPayload) => http.post<CartItemMutationResponse>("cart/items", payload),
  update: (itemId: number, payload: UpdateCartItemPayload) => http.patch<CartItemMutationResponse>(`cart/items/${itemId}`, payload),
  remove: (itemId: number) => http.delete<void>(`cart/items/${itemId}`),
};
